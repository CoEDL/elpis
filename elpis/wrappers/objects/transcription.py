from pathlib import Path
from elpis.wrappers.input.resample import resample
from elpis.wrappers.objects.command import run
from elpis.wrappers.objects.fsobject import FSObject
import threading
import subprocess
from typing import Callable
import os
from distutils import dir_util, file_util
import wave
import contextlib


class Transcription(FSObject):
    _config_file = "transcription.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_file_path = self.path.joinpath('audio.wav')
        self.model = None
        self.config["model_name"] = None
        self.config["status"] = "ready"
        self.status = "ready"
        self.type = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.audio_file_path = self.path.joinpath('audio.wav')
        self.model = None
        return self

    def link(self, model):
        self.model = model
        self.config['model_name'] = model.name

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

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
        print("********")
        print("self.hash", self.hash)
        print("spk_id", spk_id)
        print("utt_id", utt_id)
        print("rec_id", rec_id)
        print("done _generate_inference_files")

    def transcribe(self, on_complete: Callable = None):
        print("*** transcribe using long")
        self.status = "transcribing"
        self.type = "text"
        kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
        kaldi_test_path = self.model.path.joinpath('kaldi', 'data', 'test')
        kaldi_path = self.model.path.joinpath('kaldi')
        os.makedirs(f"{kaldi_infer_path}", exist_ok=True)
        dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
        file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")
        subprocess.run('sh /elpis/elpis/wrappers/inference/gmm-decode-long.sh'.split(),
                       cwd=f'{self.model.path.joinpath("kaldi")}', check=True)
        # move results
        cmd = f"cp {kaldi_infer_path}/one-best-hypothesis.txt {self.path}/ && "
        cmd += f"infer_audio_filename=$(head -n 1 {kaldi_test_path}/wav.scp | awk '{{print $2}}' |  cut -c 3- ) && "
        cmd += f"cp \"{kaldi_path}/$infer_audio_filename\" {self.path}"
        run(cmd)
        self.status = "transcribed"
        if on_complete is not None:
            on_complete()

    def transcribe_align(self, on_complete: Callable = None):

        def transcribe():
            print("*** transcribe align using long")
            kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
            os.makedirs(f"{kaldi_infer_path}", exist_ok=True)
            dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
            file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")
            subprocess.run('sh /elpis/elpis/wrappers/inference/gmm-decode-long.sh'.split(),
                           cwd=f'{self.model.path.joinpath("kaldi")}', check=True)
            file_util.copy_file(f"{kaldi_infer_path.joinpath('utterance-0.eaf')}", f'{self.path}/{self.hash}.eaf')
            self.status = "transcribed"

        def transcribe_in_background():
            transcribe()
            on_complete()

        self.status = "transcribing"
        self.type = "elan"
        if on_complete is None:
            transcribe()
        else:
            t = threading.Thread(target=transcribe_in_background)
            t.start()

    def prepare_audio(self, audio, on_complete: Callable=None):
        self._process_audio_file(audio)
        self._generate_inference_files()
        if on_complete is not None:
            on_complete()

    def text(self):
        with open(f'{self.path}/one-best-hypothesis.txt', 'rb') as fin:
            return fin.read()

    def elan(self):
        with open(f'{self.path}/{self.hash}.eaf', 'rb') as fin:
            return fin.read()
