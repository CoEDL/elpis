from pathlib import Path
from elpis.engines.common.input.resample import resample
from elpis.engines.common.input.vad import get_chunks
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.common.output.raw_to_elan import convert_raw_to_elan
import subprocess
from typing import Callable, Iterable, Tuple
import os
from distutils import dir_util, file_util
import shutil
import wave
import contextlib
import json


class EspnetTranscription(BaseTranscription):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_file_path = self.path.joinpath('audio.wav')
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.segment_data = []

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.audio_file_path = self.path.joinpath('audio.wav')
        return self

    def _build_spk2utt_file(self, spk_id: str, utt_ids: Iterable[str]):
        spk2utt_path = Path(self.path).joinpath('spk2utt')
        with spk2utt_path.open(mode='w') as fout:
            for utt_id in utt_ids:
                print(f'{spk_id} {utt_id}', file=fout)

    def _build_utt2spk_file(self, utt_ids: Iterable[str], spk_id: str):
        utt2spk_path = Path(self.path).joinpath('utt2spk')
        with utt2spk_path.open(mode='w') as fout:
            for utt_id in utt_ids:
                print(f'{utt_id} {spk_id}', file=fout)

    def _build_segments_file(self, utt_ids: Iterable[str], rec_id: str, segments: Iterable[Tuple[float, float]]):
        segments_path = Path(self.path).joinpath('segments')
        with segments_path.open(mode='w') as fout:
            for i, utt_id in enumerate(utt_ids):
                start, stop = segments[i]
                fout.write(f'{utt_id} {rec_id} {start} {stop}\n')

    def _build_wav_scp_file(self, rec_id: str, rel_audio_file_path: Path):
        wav_scp_path = Path(self.path).joinpath('wav.scp')
        with wav_scp_path.open(mode='w') as fout:
                fout.write(f'{rec_id} {rel_audio_file_path}\n')

    def _process_audio_file(self, audio):
        # TODO: maintain original audio filename
        # copy audio to the tmp folder for resampling
        tmp_path = Path(f'/tmp/{self.hash}')
        tmp_path.mkdir(parents=True, exist_ok=True)
        tmp_file_path = tmp_path.joinpath('original.wav')
        # if isinstance(audio, Path) or isinstance(audio, str):
        #     shutil.copy(f'{audio}', f'{tmp_file_path}')
        # elif isinstance(audio, BufferedIOBase):
        with tmp_file_path.open(mode='wb') as fout:
            fout.write(audio.read())
        # resample the audio file
        resample(tmp_file_path, self.path.joinpath('audio.wav'))

    def _generate_inference_files(self, utt_duration=10.0):
        """ Prepare the files we need for inference, based on the audio we receive.

            utt_duration says how long we want each utterance to be, in seconds. Long audio
            gets broken into utterances of that length.
        """
        # _process_audio_file above a file named audio.wav
        audio_file_name = 'audio.wav'
        # Get the speaker id from the model > data/test/spk2utt file. it's the first "word".
        model_spk2utt_path = Path(self.model.path).joinpath(
            'espnet-asr1/data/test/spk2utt')
        with model_spk2utt_path.open(mode='r') as fin:
            spk_id = fin.read().split()[0]
        # Duration of the audio
        abs_audio_file_path = Path(self.path).joinpath(audio_file_name)
        segments = get_chunks(abs_audio_file_path, method="duration", parameter=utt_duration)
        utt_ids = [f"{spk_id}-utterance{i:05.0f}" for i in range(len(segments))]
        self.segment_data = zip(utt_ids, segments)
        # Arbitrary id for each utterance. assuming one utterance for now
        #utt_id = spk_id + '-utterance0'

        # Rec id is arbitrary, use anything you like here
        rec_id = 'decode'
        # Path to the audio, relative to espnet working dir
        rel_audio_file_path = os.path.join('data', 'infer', audio_file_name)
        # Generate the files
        self._build_spk2utt_file(spk_id, utt_ids)
        self._build_utt2spk_file(utt_ids, spk_id)
        self._build_segments_file(utt_ids, rec_id, segments)
        self._build_wav_scp_file(rec_id, rel_audio_file_path)
        self.rel_audio_file_path = rel_audio_file_path

    def transcribe(self, on_complete: Callable = None):
        self.status = "transcribing"
        infer_path = self.model.path.joinpath('espnet-asr1', 'data', 'infer')
        exp_path = self.model.path.joinpath('espnet-asr1', 'exp')
        os.makedirs(f"{infer_path}", exist_ok=True)
        dir_util.copy_tree(f'{self.path}', f"{infer_path}")
        file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('espnet-asr1', 'audio.wav')}")
        local_espnet_path = Path(self.model.path) / "espnet-asr1" # TODO This is now not a single point of control. Make this dir an attribute of the model.
        prepare_log_path = Path(self.model.path) / "prepare_transcribe_log.txt"
        transcribe_log_path = Path(self.model.path) / "transcribe_log.txt"
        from elpis.engines.common.objects.command import run
        run(f"cd {local_espnet_path}; ./decode.sh --nj 1 --stage 0 --stop_stage 2 --recog_set infer &> {prepare_log_path}")
        run(f"cd {local_espnet_path}; ./decode.sh --nj 1 --stage 5 --recog_set infer &> {transcribe_log_path}")
        result_paths = list(exp_path.glob("train_nodev*/decode_infer*"))
        assert len(result_paths) == 1, f"Incorrect number of result files ({len(result_paths)})"
        result_path = result_paths[0] / "data.json"
        self.result_path = file_util.copy_file(result_path, f'{self.path}/results.txt')[0]
        self.convert_to_text()
        self.convert_to_elan()
        self.status = "transcribed"
        if on_complete is not None:
            on_complete()

    def prepare_audio(self, audio, on_complete: Callable = None):
        self._process_audio_file(audio)
        self._generate_inference_files()
        if on_complete is not None:
            on_complete()

    def text(self):
        with open(self.text_path, 'r') as fin:
            text = fin.read()
            return text

    def elan(self):
        with open(self.elan_path, 'r') as fin:
            return fin.read()

    def convert_to_text(self):
        with open(self.result_path, 'r') as fin:
            data = json.load(fin)
        lines = [output["rec_text"].replace("<eos>", "\n") for utt_key, utt_data in data["utts"].items() for output in utt_data["output"]]
        with open(self.text_path, 'w') as fout:
            fout.writelines(lines)

    def convert_to_elan(self):
        self.retrieve_transcription_data()
        convert_raw_to_elan(self.transcription_data, self.xml_path, self.elan_path)

    def retrieve_transcription_data(self):
        with open(self.result_path, "r") as result_file:
            results = json.load(result_file)
        segment_data = [
            {"segment": {
                "id": utterance,
                "utterance id": utterance.split("-")[-1],
                "speaker id": "-".join(utterance.split("-")[0:-1]),
                "text": results["utts"][utterance]["output"][0]["rec_text"],  # Need to know if output contains only 1 dict…
                "start": segment[0],
                "end": segment[1],
                "score": results["utts"][utterance]["output"][0]["score"]}  # See above.
            } for utterance, segment in self.segment_data if utterance in results["utts"]]  # It seems it can have more segments than utterances…
        self.transcription_data = {
            "author": "elpis-espnet",
            "participant": "unknown",
            "audio path": self.audio_file_path,
            "relative audio path": self.rel_audio_file_path,
            "version": 2.8,
            "tier id": "default",
            "source language code": "",
            "segments": segment_data}
