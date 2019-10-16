from pathlib import Path
from elpis.wrappers.input.resample import resample
from elpis.wrappers.inference.generate_infer_files import generate_files
from elpis.wrappers.objects.command import run
from elpis.wrappers.objects.fsobject import FSObject
# import shutil
import threading
import subprocess
from typing import Callable
import os
import distutils.dir_util

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
        self._exporter = None
        self.config['exporter'] = None
        self.config['has_been_transcribed'] = False

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.audio_file_path = self.path.joinpath('audio.wav')
        self.model = None

        self._exporter = self.config['exporter']
        if self._exporter != None:
            exporter_name = self._exporter['name']
            self.select_exporter(exporter_name)
        return self

    def link(self, model):
        self.model = model
        self.config['model_name'] = model.name

    @property
    def status(self):
        return self.config['status']
    
    @property
    def state(self):
        return {
            'name': self.config['name'],
            'hash': self.config['hash'],
            'date': self.config['date'],
            'model': self.config['model_name'],
            'has_been_transcribed': self.config['has_been_transcribed'],
            'exporter': self.config['exporter']
        }
    
    @property
    def has_been_transcribed(self):
        return self.config['has_been_transcribed']
    
    @property
    def exporter(self):
        return self._exporter

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def _process_audio_file(self, audio):
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

    def _bake_gmm_decode_align(self):
        with open('/workspaces/elpis/elpis/wrappers/inference/gmm-decode-align.sh', 'r') as fin:
            content: str = fin.read()
        content = content.replace('/elpis/elpis/wrappers/output/ctm_to_textgrid.py',
                                  '/workspaces/elpis/elpis/wrappers/output/ctm_to_textgrid.py')
        content = content.replace('/elpis/elpis/wrappers/output/textgrid_to_elan.py',
                                  '/workspaces/elpis/elpis/wrappers/output/textgrid_to_elan.py')
        decode_file_path = self.path.joinpath('gmm-decode-align.sh')
        with decode_file_path.open(mode='w') as file_:
            file_.write(content)
        run(f'chmod +x {decode_file_path}')

        p = subprocess.run(f'sh {decode_file_path}'.split(), cwd=f'{self.model.path.joinpath("kaldi")}', check=True)

    def transcribe_to_text(self, audio_file_path: str):
        if self.model == None:
            raise RuntimeError('must link model before transcribing text')
        # copy the audio file
        with self.audio_file_path.open('wb') as fout:
            with open(audio_file_path, 'rb') as fin:
                fout.write(fin.read())
        kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
        kaldi_test_path = self.model.path.joinpath('kaldi', 'data', 'test')
        kaldi_path = self.model.path.joinpath('kaldi')
        os.makedirs(f"{kaldi_infer_path}", exist_ok=True)
        distutils.dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
        distutils.file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")

        subprocess.run('sh /workspaces/elpis/elpis/wrappers/inference/gmm-decode.sh'.split(),
                       cwd=f'{self.model.path.joinpath("kaldi")}', check=True)

        # move results
        cmd = f"cp {kaldi_infer_path}/one-best-hypothesis.txt {self.path}/ && "
        cmd += f"infer_audio_filename=$(head -n 1 {kaldi_test_path}/wav.scp | awk '{{print $2}}' |  cut -c 3- ) && "
        cmd += f"cp \"{kaldi_path}/$infer_audio_filename\" {self.path}"
        run(cmd)
        return self.text()

    def transcribe_align(self, audio_file_path: str):
        if self.model == None:
            raise RuntimeError('must link model before transcribe align')
        self.status = "transcribing"
        self.type = "align"
        
        # copy the audio file
        with self.audio_file_path.open('wb') as fout:
            with open(audio_file_path, 'rb') as fin:
                fout.write(fin.read())
        
        kaldi_infer_path = self.model.path.joinpath('kaldi', 'data', 'infer')
        os.makedirs(f"{kaldi_infer_path}", exist_ok=True) # TODO: the dir already exists and belongs to the model, review this and remove this line.
        distutils.dir_util.copy_tree(f'{self.path}', f"{kaldi_infer_path}")
        distutils.file_util.copy_file(f'{self.audio_file_path}', f"{self.model.path.joinpath('kaldi', 'audio.wav')}")

        self._bake_gmm_decode_align()
        # p = subprocess.run('sh /kaldi-helpers/kaldi_helpers/inference/gmm-decode-align.sh'.split(),
        # cwd=f'{self.model.path.joinpath("kaldi")}')

        # move results
        # cmd = f"cp {kaldi_infer_path}/one-best-hypothesis.txt {self.path}/ && "
        # cmd += f"infer_audio_filename=$(head -n 1 {kaldi_test_path}/wav.scp | awk '{{print $2}}' |  cut -c 3- ) && "
        # cmd += f"cp \"{kaldi_path}/$infer_audio_filename\" {self.path}"
        # run(cmd)
        distutils.file_util.copy_file(f"{kaldi_infer_path.joinpath('utterance-0.eaf')}", f'{self.path}/{self.hash}.eaf')
        self.status = "transcribed"
        return

    def prepare_audio(self, audio, on_complete: Callable=None):
        self._process_audio_file(audio)
        generate_files(self)
        if on_complete is not None:
            on_complete()

    def text(self):
        with open(f'{self.path}/one-best-hypothesis.txt', 'r') as fin:
            return fin.read()

    def elan(self):
        with open(f'{self.path}/{self.hash}.eaf', 'rb') as fin:
            return fin.read()
