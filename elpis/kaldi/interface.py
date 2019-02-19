import os
import json
from . import hasher
from pathlib import Path
from appdirs import user_data_dir
from .dataset import Dataset
from .logger import Logger
from .model import Model
from .transcription import Transcription
from .fsobject import FSObject

Path().parent

class KaldiInterface(FSObject):
    def __init__(self, path: Path = None, name: str = None):
        self._config_file = 'interface.json'
        if path is None:
            name = hasher.new()
            super().__init__(
                parent_path=Path(user_data_dir('elpis')),
                dir_name = name,
                pre_allocated_hash=name,
                name=name
            )
        else:
            path = Path(path).absolute()
            super().__init__(
                parent_path=path.parent,
                dir_name=path.name,
                name=name
            )
        # ensure object directories exist
        self.datasets_path = self.path.joinpath('datasets')
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.models_path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.loggers_path = self.path.joinpath('loggers')
        self.loggers_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        # config objects
        self.loggers = []
        self.datasets = {}
        self.models = {}
        self.transcriptions = {}
        self.interface_path = self.path.joinpath('interface.json')

        self.config['loggers'] = []
        self.config['datasets'] = []
        self.config['models'] = []
        self.config['transcriptions'] = []
        

        # make a default logger
        self.new_logger(default=True)

    def _edit_interface_config(self, key, value):
        with open(self.interface_path, 'r') as fin:
            config = json.load(fin)
        config[key].append(value)
        with open(self.interface_path, 'w') as fout:
            json.dump(config, fout)

    def new_logger(self, default=False):
        logger = Logger(self.loggers_path)
        self._edit_interface_config('loggers', logger.hash)
        if default:
            self.logger = logger
        return logger

    def new_dataset(self, dsname):
        ds = Dataset(self.datasets_path, dsname, self.logger)
        self._edit_interface_config('datasets', {
            dsname: ds.hash
        })
        return ds

    def get_dataset(self, dsname):
        return

    def list_datasets(self):
        return

    def new_model(self, mname):
        m = Model(self.models_path, mname, self.logger)
        self._edit_interface_config('models', {
            mname: m.hash
        })
        return m

    def get_model(self, mname):
        return

    def list_models(self):
        return

    def new_transcription(self, tname, model):
        t = Transcription(self.transcriptions_path, tname, self.logger, model)
        self._edit_interface_config('transcriptions', {
            tname: t.hash
        })
        return t

    def get_transcription(self, tname):
        return

    def list_transcriptions(self):
        return
