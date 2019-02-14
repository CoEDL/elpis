import json
import os
from .fsobject import FileSystemObject
from . import task

class status:
    UNPROCESSED = 'unprocessed'

class DataBundle(FileSystemObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def add(self, fp, name=None):
        data_path = f'{self._working_path}/data'
        if not os.path.exists(data_path):
            os.mkdir(data_path)
        if name == None:
            name = fp.name
        name = os.path.basename(name)
        with open(f'{data_path}/{name}', 'wb') as fout:
            fout.write(fp.read())
        self.sync_to_kaldi()
    
    def prepare(self):
        task('clean-output-folder tmp-makedir make-kaldi-subfolders')
        task('elan-to-json')
        task('clean-json')
        task('process-audio')
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
        with open(f'{self._kaldi_path}/wordlist.json', 'w') as fout:
            json.dump(wordlist, fout)
        self.sync_to_working()
