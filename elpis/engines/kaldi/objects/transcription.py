from pathlib import Path
from elpis.engines.common.input.resample import resample
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
import subprocess
from typing import Callable, Dict
import os
from distutils import dir_util, file_util
import wave
import contextlib


class KaldiTranscription(BaseTranscription):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config['stage_status'] = {}
        stage_names = {
            "0_feature_vec.sh": "Extracting feature vectors",
            "1_cmvn.sh": "Applying CMVN",
            "2_transcription_decode.sh": "Decoding (transcription)",
            "3_transcription_best_path.sh": "Finding best path (transcription)",
            "4_word_boundaries.sh": "Adding word boundaries to FST",
            "5_lattice_to_ctm.sh": "Converting lattice to CTM",
            "6_word_idx_to_words.sh": "Translating word indexes to words",
            "7_ctm_textgrid.sh": "Converting CTM to Textgrid",
            "8_textgrid_elan.sh": "Converting Textgrid to ELAN",
            "9_ctm_output.sh": "CTM output"
        }
        self.build_stage_status(stage_names)
        self.audio_file_path = self.path.joinpath('audio.wav')

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.audio_file_path = self.path.joinpath('audio.wav')
        return self

    def _build_spk2utt_file(self, spk_id: str, utt_id: str):
        spk2utt_path = Path(self.path).joinpath('spk2utt')
        with spk2utt_path.open(mode='w') as fout:
                fout.write(f'{spk_id} {utt_id}\n')

    def _build_utt2spk_file(self, utt_id: str, spk_id: str):
        utt2spk_path = Path(self.path).joinpath('utt2spk')
        with utt2spk_path.open(mode='w') as fout:
                fout.write(f'{utt_id} {spk_id}\n')

    def _build_segments_file(self, utt_id: str, rec_id: str, start_ms: float, stop_ms: float):
        segments_path = Path(self.path).joinpath('segments')
        with segments_path.open(mode='w') as fout:
                fout.write(f'{utt_id} {rec_id} {start_ms} {stop_ms}\n')

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

    # Prepare the files we need for inference, based on the audio we receive
    def _generate_inference_files(self):
        # _process_audio_file above a file named audio.wav
        audio_file_name = 'audio.wav'
        # Get the speaker id from the model > kaldi/data/test/spk2utt file. it's the first "word".
        model_spk2utt_path = Path(self.model.path).joinpath(
            'kaldi/data/test/spk2utt')
        with model_spk2utt_path.open(mode='r') as fin:
            spk_id = fin.read().split()[0]
        # Arbitrary id for each utterance. assuming one utterance for now
        utt_id = spk_id + '-utterance0'
        # Expecting to start at 0 time. Could benefit from VAD here?
        start_ms = 0.00
        # Duration of the audio
        abs_audio_file_path = Path(self.path).joinpath(audio_file_name)
        with contextlib.closing(wave.open(str(abs_audio_file_path), 'r')) as fin:
            frames = fin.getnframes()
            rate = fin.getframerate()
            stop_ms = frames / float(rate)
        # Rec id is arbitrary, use anything you like here
        rec_id = 'decode'
        # Path to the audio, relative to kaldi working dir
        rel_audio_file_path = os.path.join('data', 'infer', audio_file_name)
        # Generate the files
        self._build_spk2utt_file(spk_id, utt_id)
        self._build_utt2spk_file(utt_id, spk_id)
        self._build_segments_file(utt_id, rec_id, start_ms, stop_ms)
        self._build_wav_scp_file(rec_id, rel_audio_file_path)

    def transcribe(self, on_complete: Callable = None):
        self.status = "transcribing"
        kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
        gmm_decode_path = Path('/elpis/elpis/engines/kaldi/inference/gmm-decode')
        os.makedirs(f"{kaldi_infer_path}", exist_ok=True)
        dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
        file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")
        dir_util.copy_tree(gmm_decode_path, f"{kaldi_infer_path.joinpath('gmm-decode')}")
        subprocess.run('sh /elpis/elpis/engines/kaldi/inference/gmm-decode-long.sh'.split(),
                       cwd=f'{self.model.path.joinpath("kaldi")}', check=True)
        file_util.copy_file(f"{kaldi_infer_path.joinpath('one-best-hypothesis.txt')}", f'{self.path}/one-best-hypothesis.txt')
        file_util.copy_file(f"{kaldi_infer_path.joinpath('utterance-0.eaf')}", f'{self.path}/{self.hash}.eaf')
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
            return fin.read()

    def elan(self):
        with open(f'{self.path}/{self.hash}.eaf', 'rb') as fin:
            return fin.read()

    def build_stage_status(self, stage_names: Dict[str, str]):
        for stage_file, stage_name in stage_names.items():
            stage_status = self.config['stage_status']
            stage_status.update({stage_file: {'name': stage_name, 'status': 'ready', 'message': ''}})
            self.config['stage_status'] = stage_status