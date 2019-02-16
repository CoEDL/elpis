import json
import os
from .fsobject import FileSystemObject
from .util import task

class status:
    UNPROCESSED = 'unprocessed'

class DataBundle(FileSystemObject):
    def __init__(self, kaldi, description: str, working_path: str, save_path: str, kaldi_path: str, *args, **kwargs):
        super().__init__(kaldi, description, working_path, save_path, kaldi_path, *args, **kwargs)
    
    def add(self, fp, name=None):
        if name == None:
            name = fp.name
        name = os.path.basename(name)
        with open(f'{self._working_path}/{name}', 'wb') as fout:
            fout.write(fp.read())
        self.sync_to_kaldi()
    
    def list_files(self):
        sx = []
        for obj in os.listdir(self._working_path):
            if obj.endswith('.txt') or obj == "wordlist.json":
                continue
            else:
                sx.append(obj)
        return sx
    
    def prepare(self):
        task('clean-output-folder tmp-makedir make-kaldi-subfolders')
        task('elan-to-json')
        task('clean-json')
        task('process-audio')
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
    
    def get_wordlist(self):
        # TODO: unimplemented
        pass
    

