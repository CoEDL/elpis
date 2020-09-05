from pathlib import Path
from elpis.engines.common.input.resample import resample
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
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

            utt_duration says how long we want each utterance to be, in ms. Long audio
            gets broken into utterances of that length.
        """
        # _process_audio_file above a file named audio.wav
        audio_file_name = 'audio.wav'
        # Get the speaker id from the model > data/test/spk2utt file. it's the first "word".
        model_spk2utt_path = Path(self.model.path).joinpath(
            'espnet-asr1/data/test/spk2utt')
        with model_spk2utt_path.open(mode='r') as fin:
            spk_id = fin.read().split()[0]
        # Expecting to start at 0 time. Could benefit from VAD here?
        start = 0.00
        # Duration of the audio
        abs_audio_file_path = Path(self.path).joinpath(audio_file_name)
        with contextlib.closing(wave.open(str(abs_audio_file_path), 'r')) as fin:
            frames = fin.getnframes()
            rate = fin.getframerate()
            stop = frames / float(rate)

        num_utters = int(stop / utt_duration) + 1
        utt_ids = [f"{spk_id}-utterance{i:05.0f}" for i in range(num_utters)]
        segments = [(i*utt_duration, (i+1)*utt_duration - 0.001) for i in range(num_utters)]
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
        assert len(result_paths) == 1, f"Incorrect number of result files ({len(result_path)})"
        result_path = result_paths[0] / "data.json"
        file_util.copy_file(result_path, f'{self.path}/results.txt')
        self.convert_to_text()
        # TODO Need to produce an output eaf.
        self.status = "transcribed"
        if on_complete is not None:
            on_complete()

    def prepare_audio(self, audio, on_complete: Callable = None):
        self._process_audio_file(audio)
        self._generate_inference_files()
        if on_complete is not None:
            on_complete()

    def text(self):
        with open(f'{self.path}/one-best-hypothesis.txt', 'r') as fin:
            text = fin.read()
            print(text)
            print(self.path)
            return text

    def elan(self):
        # TODO once I know more about temporal data from ESPNet. For now, it targets the txt file.
        with open(f'{self.path}/one-best-hypothesis.txt', 'r') as fin:
            return fin.read()

    def convert_to_text(self):
        with open(f'{self.path}/results.txt', 'r') as fin:
            data = json.load(fin)
        lines = [output["rec_text"].replace("<eos>", "\n") for utt_key, utt_data in data["utts"].items() for output in utt_data["output"]]
        with open(f'{self.path}/one-best-hypothesis.txt', 'w') as fout:
            fout.writelines(lines)

    def convert_to_elan(self):
        self.convert_to_text()  #TODO
