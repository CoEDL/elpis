import os
import json
from . import hasher
from pathlib import Path
from appdirs import user_data_dir
from .dataset import Dataset
from .session import Session

class KaldiInterface(object):
    def __init__(self, path:Path=None, name:str=None):
        super().__init__()
        #
        if name is None:
            self.name = hasher.new()
        # set app data path
        if path is None:
            self.path = Path(user_data_dir('elpis')).joinpath(self.name)
        else:
            self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        # ensure object directories exist
        self.datasets_path = self.path.joinpath('datasets')
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.models_path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.sessions_path = self.path.joinpath('sessions')
        self.sessions_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        # config objects
        self.sessions = []
        self.datasets = {}
        self.models = {}
        self.transcriptions = {}
        self.interface_path = self.path.joinpath('interface.json')
        if not os.path.exists(self.interface_path):
            with open(self.interface_path, 'w') as fout:
                config = {
                    'sessions': [],
                    'datasets': [],
                    'models': [],
                    'transcriptions': []
                }
                json.dump(config, fout)

        # make a default session
        self.new_session(default=True)

    def _edit_interface_config(self, key, value):
        with open(self.interface_path, 'r') as fin:
            config = json.load(fin)
        config[key].append(value)
        with open(self.interface_path, 'w') as fout:
            json.dump(config, fout)

    def new_session(self, default=False):
        s = Session(self.sessions_path)
        self._edit_interface_config('sessions', s.hash)
        if default:
            self.session = s
        return s

    def new_dataset(self, dsname):
        ds = Dataset(self.datasets_path, dsname, self.session)
        self._edit_interface_config('datasets', {
            dsname: ds.hash
        })
        return ds
    def get_dataset(self, dsname):
        return
    def list_datasets(self):
        return