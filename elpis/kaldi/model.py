import hashlib
import json
import os
import time
import shutil
from typing import List, Tuple

from . import step, KaldiError, task
from .. import paths
from .fsobject import FileSystemObject

class Model(FileSystemObject):
    # File is (filename, contents)
    File = Tuple[str, str]
    FilePair = Tuple[File, File]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_status(self, directory) -> str:
        def no_model() -> bool:
            return not os.path.exists(directory) or (
                len(os.listdir(directory)) == 0
            )
        def complete_model() -> bool:
            return sorted(os.listdir(directory)) == sorted([
                    'data',
                    'config',
                    'name.txt',
                    'date.txt',
                    'hash.txt',
                    'wordlist.json',
                ]) and (
                    len(os.listdir(f'{directory}/data')) != 0 and sorted([
                        'letter_to_sound.txt',
                        'optional_silence.txt',
                        'silence_phones.txt'
                    ]) == sorted(os.listdir(f'{directory}/config'))
                )
        if no_model(): return 'No Model'
        elif not complete_model(): return 'Incomplete Model'
        else: return 'Untrained Model'

    def get_info_of(self, name):
        # TODO: unimplemented
        return {}

    def load_transcription_files(self, file_pairs: List[FilePair]):
        """
        :param file_pairs: is a list of paired tuples of tuples... file_pairs is
        a list of (FILE, FILE), while FILE is a tuple representing a file by
        (filename, filecontent).
        """
        if not os.path.exists(f'{self._working_path}/data'):
            os.mkdir(f'{self._working_path}/data')
        for pair in file_pairs:
            for filename, filecontent in pair:
                with open(f'{self._working_path}/data/{filename}', 'wb') as fout:
                    fout.write(filecontent)
        self.sync_to_kaldi()

    def get_transcription_files(self) -> List[str]:
        return [ name for name in os.listdir(f'{self._working_path}/data')]

    def generate_word_list(self):
        # only steps 1 and 2 of _run-elan
        task('clean-output-folder tmp-makedir make-kaldi-subfolders')
        task('elan-to-json')
        self.sync_to_working()
        wordlist = {}
        path = f'{self._kaldi_path}/output/tmp/dirty.json'
        with open(path, 'r') as fin:
            dirty = json.load(fin)
        for transcription in dirty:
            words = transcription['transcript'].split()
            for word in words:
                if word in wordlist:
                    wordlist[word] += 1
                else:
                    wordlist[word] = 1
        with open(f'{self._working_path}/wordlist.json', 'w') as fout:
            json.dump(wordlist, fout)
        self.sync_to_kaldi()

    def get_wordlist(self) -> str:
        if os.path.exists(f'{self._working_path}/wordlist.json'):
            with open(f'{self._working_path}/wordlist.json', 'r') as fin:
                return fin.read()
        return None

    def load_pronunciation_dictionary(filecontent):
        # TODO: unimplemented
        return ''

    def get_pronunciation_dictionary():
        """
        :return: None if the pronunciation dictionary has yet to be loaded,
        otherwise, the content of the pronunciation dictionary is returned
        """
        # TODO: unimplemented
        return None

    def load_settings(file):
        # TODO: unimplemented
        return ''

    def get_settings():
        # TODO: unimplemented
        return None

    def train():
        # TODO: unimplemented
        return ''
        # TODO: unimplemented
        return None

    def get_training_results():
        # TODO: unimplemented
        return None