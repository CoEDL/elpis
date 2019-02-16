import os
import shutil
import sys
from pathlib import Path

class Context(object):
    def __init__(self, object_type, object_name, **kwargs):
        super().__init__()
        self.path_working = Path('./test_object_working')
        self.path_save = Path('./test_object_save')
        self.path_kaldi = Path('./test_object_kaldi')
        self.object_type = object_type
        self.object_name = object_name
        self._kwargs = kwargs

    def clear_dir(self, path: Path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def touch(self, path):
        contents = ''
        if os.path.exists(path):
            with open(path, 'r') as fin:
                contents = fin.read()
        with open(path, 'w') as fout:
            fout.write(contents)

    def __call__(self, f):
        def wrapper():
            obj = self.object_type(None, self.object_name, self.path_working, self.path_save, self.path_kaldi, **self._kwargs)
            self.clear_dir(self.path_working)
            self.clear_dir(self.path_save)
            self.clear_dir(self.path_kaldi)
            f(obj)
            if self.path_working.exists():
                shutil.rmtree(self.path_working)
            if self.path_save.exists():
                shutil.rmtree(self.path_save)
            if self.path_kaldi.exists():
                shutil.rmtree(self.path_kaldi)
        return wrapper
    
    @property
    def path_working(self):
        return self.__path_working
    
    @path_working.setter
    def path_working(self, path: Path):
        self.__path_working = Path(path)

    @property
    def path_save(self):
        return self.__path_save
    
    @path_save.setter
    def path_save(self, path: Path):
        self.__path_save = Path(path)

    @property
    def path_kaldi(self):
        return self.__path_kaldi
    
    @path_kaldi.setter
    def path_kaldi(self, path: Path):
        self.__path_kaldi = Path(path)
