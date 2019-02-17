import time
import os
import json
from . import hasher
from .command import run
from pathlib import Path
from typing import List
from .session import Session
from io import BufferedIOBase
from kaldi_helpers.input_scripts import process_eaf, clean_json_data, process_item

class Dataset(object):
    def __init__(self, basepath:Path, name:str, sesson: Session):
        super().__init__()
        self.name: str = name
        self.hash: str = hasher.new()
        self.files: List[Path] = []

        # paths
        self.path: Path = basepath.joinpath(self.hash)
        self.path.mkdir(parents=True, exist_ok=True)
        self.data_path: Path = self.path.joinpath('original')
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.elan_json_path: Path = self.path.joinpath('elan.json')
        self.resampled_path: Path = self.path.joinpath('resampled')
        self.resampled_path.mkdir(parents=True, exist_ok=True)

        # additional attributes
        self.has_been_processed = False
        self.session = sesson
        self.tier = 'Phrase'

        # config
        self.config_path = self.path.joinpath('dataset.json')
        """
        {
            name: str,
            hash: hash,
            files: [Path],
            path: str,
            session: hash,
        }
        """
        config = {
            'name': name,
            'hash': self.hash,
            'files': [],
            'has_been_processed': False,
            'session': self. session.hash,
            'tier': self.tier
        }
        self._write_config(config)

    def add(self, audio_file: Path, transc_file: Path):
        audio_path = Path(audio_file)
        transc_path = Path(transc_file)
        aname = audio_path.name
        tname = transc_path.name
        with audio_path.open(mode='rb') as fa:
            with transc_path.open(mode='rb') as ft:
                self.add_fp(fa, ft, aname, tname)

    def add_fp(self, audio_fp: BufferedIOBase, transc_fp: BufferedIOBase, audio_name: str, transc_name: str):
        a_out: Path = self.data_path.joinpath(audio_name)
        t_out: Path = self.data_path.joinpath(transc_name)
        with a_out.open(mode='wb') as faout:
            faout.write(audio_fp.read())
        with t_out.open(mode='wb') as ftout:
            ftout.write(transc_fp.read())
        self.files.append(a_out)
        self.files.append(t_out)
        config = self._read_config()
        config['files'] = [f'{f.name}' for f in self.files]
        self._write_config(config)
    
    def _read_config(self):
        with self.config_path.open() as fin:
            return json.load(fin)

    def _write_config(self, config):
        with self.config_path.open(mode='w') as fout:
            json.dump(config, fout)
    
    def process(self):
        dirty = []
        for file in self.files:
            if file.name.endswith('.eaf'):
                obj = process_eaf(f'{file.absolute()}', self.tier)
                dirty.extend(obj)
        # TODO other options for the command below: remove_english=arguments.remove_eng, use_langid=arguments.use_lang_id
        filtered = clean_json_data(json_data=dirty)
        with self.elan_json_path.open(mode='w') as fout:
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


        base_directory = f'{self.data_path}'
        audio_extensions = {"*.wav"}
        temporary_directory_path = Path(f'/tmp/{self.hash}/working')
        temporary_directory_path.mkdir(parents=True, exist_ok=True)
        temporary_directory = f'{temporary_directory_path}'

        all_files_in_dir = glob.glob(os.path.join(base_directory, "**"), recursive=True)
        input_audio = [ file_ for file_ in all_files_in_dir if file_.endswith(".wav")]
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
                move(audio_file, self.resampled_path)
                # file_name = os.path.basename(audio_file)
                # parent_directory = os.path.dirname(os.path.dirname(audio_file))
                # move(audio_file, os.path.join(parent_directory, file_name))
            # Clean up tmp folders
            for d in temporary_directories:
                os.rmdir(d)
        # p = run(f"cd {self.resampled_path}; tar cf {self.path}/media.tar `find . | grep '\.wav'`")
        # print(p.stdout.decode('utf-8'))

    # TODO: additional text
