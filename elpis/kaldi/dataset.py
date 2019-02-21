import time
import os
import json
import shutil 

from pathlib import Path
from typing import List
from io import BufferedIOBase

from . import hasher
from .command import run
from .logger import Logger
from .fsobject import FSObject
from .path_structure import existing_attributes, ensure_paths_exist

from kaldi_helpers.input_scripts.elan_to_json import process_eaf
from kaldi_helpers.input_scripts.clean_json import clean_json_data
from kaldi_helpers.input_scripts.resample_audio import process_item

DEFAULT_TIER = 'Phrase'

class DSPaths(object):
    def __init__(self, basepath: Path):
        # directories
        attrs = existing_attributes(self)
        self.basepath = basepath
        self.original = self.basepath.joinpath('original')
        self.resampled = self.basepath.joinpath('resampled')
        ensure_paths_exist(self, attrs)

        # files
        self.filtered_json: Path = self.basepath.joinpath('filtered.json')


class Dataset(FSObject):
    _config_file = 'dataset.json'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__files: List[Path] = []
        self.pathto = DSPaths(self.path)
        self.has_been_processed = False

        # config
        self.config['tier'] = DEFAULT_TIER
        self.config['has_been_processed'] = False
        self.config['files'] = []

    @classmethod
    def load(cls, basepath: Path):
        self = super().load(basepath)
        self.__files = [Path(path) for path in self.config['files']]
        self.pathto = DSPaths(self.path)
        self.has_been_processed = self.config['has_been_processed']
        return self
    
    @property
    def tier(self) -> str:
        return self.config['tier']

    @tier.setter
    def tier(self, value: str):
        self.config['tier'] = value
    
    @property
    def files(self):
        return self.config['files']

    def add_elan_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return
    def add_textgrid_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return
    def add_transcriber_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return

    def add_wave_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return
    def add_other_audio_type_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return
    
    def list_audio_files(self) -> List[str]:
        # TODO: unimplemented!
        return
    def list_transcription_files(self) -> List[str]:
        # TODO: unimplemented!
        return
    def list_all_files(self) -> List[str]:
        # TODO: unimplemented!
        return

    
    def remove_file(self, filename) -> None:
        # TODO: unimplemented!
        return

    def add(self, audio_file: Path, transc_file: Path):
        audio_path = Path(audio_file)
        transc_path = Path(transc_file)
        aname = audio_path.name
        tname = transc_path.name
        with audio_path.open(mode='rb') as fa:
            with transc_path.open(mode='rb') as ft:
                self.add_fp(fa, ft, aname, tname)

    def add_fp(self, audio_fp: BufferedIOBase, transc_fp: BufferedIOBase, audio_name: str, transc_name: str):
        a_out: Path = self.pathto.original.joinpath(audio_name)
        t_out: Path = self.pathto.original.joinpath(transc_name)
        with a_out.open(mode='wb') as faout:
            faout.write(audio_fp.read())
        with t_out.open(mode='wb') as ftout:
            ftout.write(transc_fp.read())
        self.__files.append(a_out)
        self.__files.append(t_out)
        self.config['files'] += [f'{f.name}' for f in self.__files]

    def process(self):
        # remove existing file in resampled
        # TODO check what other files need removing
        shutil.rmtree(f'{self.pathto.resampled}')
        self.pathto.resampled.mkdir(parents=True, exist_ok=True)
        # process files
        dirty = []
        for file in self.__files:
            if file.name.endswith('.eaf'):
                obj = process_eaf(f'{self.pathto.original.joinpath(file)}', self.tier)
                dirty.extend(obj)
        # TODO other options for the command below: remove_english=arguments.remove_eng, use_langid=arguments.use_lang_id
        filtered = clean_json_data(json_data=dirty)
        with self.pathto.filtered_json.open(mode='w') as fout:
            json.dump(filtered, fout)

        import argparse
        import glob
        import os
        import subprocess
        import threading
        from multiprocessing.dummy import Pool
        from shutil import move
        from typing import Set, Tuple
        from kaldi_helpers.script_utilities import find_files_by_extensions
        from kaldi_helpers.script_utilities.globals import SOX_PATH

        base_directory = f'{self.pathto.original}'
        audio_extensions = {"*.wav"}
        temporary_directory_path = Path(f'/tmp/{self.hash}/working')
        temporary_directory_path.mkdir(parents=True, exist_ok=True)
        temporary_directory = f'{temporary_directory_path}'

        all_files_in_dir = glob.glob(os.path.join(
            base_directory, "**"), recursive=True)
        input_audio = [
            file_ for file_ in all_files_in_dir if file_.endswith(".wav")]
        process_lock = threading.Lock()
        temporary_directories = set()

        map_arguments = [(index, audio_path, process_lock, temporary_directories, temporary_directory)
                         for index, audio_path in enumerate(input_audio)]
        # Multi-Threaded Audio Re-sampling
        with Pool() as pool:
            outputs = pool.map(process_item, map_arguments)
            # TODO: overwrite?
            # Replace original files
            for audio_file in outputs:
                move(audio_file, self.pathto.resampled)
                # file_name = os.path.basename(audio_file)
                # parent_directory = os.path.dirname(os.path.dirname(audio_file))
                # move(audio_file, os.path.join(parent_directory, file_name))
            # Clean up tmp folders
            for d in temporary_directories:
                os.rmdir(d)
        self.config['has_been_processed'] = True
