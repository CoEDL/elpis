import os
import json
from . import hasher
from pathlib import Path
from appdirs import user_data_dir
from .errors import KaldiError
from .dataset import Dataset
from .logger import Logger
from .model import Model
from .transcription import Transcription
from .fsobject import FSObject


class KaldiInterface(FSObject):
    _config_file = 'interface.json'
    def __init__(self, path: Path = None):
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
                dir_name=path.name
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

        self.config['loggers'] = []
        self.config['datasets'] = {}
        self.config['models'] = {}
        self.config['transcriptions'] = {}


        # make a default logger
        self.new_logger(default=True)

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
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
        return self


    def new_logger(self, default=False):
        logger = Logger(self.loggers_path)
        self.config['loggers'] += [logger.hash]
        if default:
            self.logger = logger
        return logger

    def new_dataset(self, dsname):
        existing_names = self.list_datasets()
        if dsname in self.config['datasets'].keys():
            raise KaldiError(
                f'Tried adding \'{dsname}\' which is already in {existing_names} with hash {self.config["datasets"][dsname]}.',
                human_message=f'data bundle with name "{dsname}" already exists'
            )
        ds = Dataset(parent_path=self.datasets_path, name=dsname, logger=self.logger)
        datasets = self.config['datasets']
        datasets[dsname] = ds.hash
        self.config['datasets'] = datasets
        return ds

    def get_dataset(self, dsname):
        if dsname not in self.list_datasets():
            raise KaldiError(f'Tried to load a dataset called "{dsname}" that does not exist')
        hash_dir = self.config['datasets'][dsname]
        return Dataset.load(self.datasets_path.joinpath(hash_dir))

    def list_datasets(self):
        names = [name for name in self.config['datasets'].keys()]
        return names

    def new_model(self, mname):
        m = Model(parent_path=self.models_path, name=mname, logger=self.logger)
        models = self.config['models']
        models[mname] = m.hash
        self.config['models'] = models
        return m

    def get_model(self, mname):
        return

    def list_models(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            with self.models_path.joinpath(hash_dir, Model._config_file).open() as fin:
                name = json.load(fin)['name']
                # TODO: replace with model training results
                results = { 'wer': 1, 'del': 1, 'ins': 2, 'sub': 3 }
                model = {'name': name, 'results': results}
                models.append(model)
        return models

    def new_transcription(self, tname):
        t = Transcription(parent_path=self.transcriptions_path, name=tname, logger=self.logger)
        transcriptions = self.config['transcriptions']
        transcriptions[tname] = t.hash
        self.config['transcriptions'] = transcriptions
        return t

    def get_transcription(self, tname):
        return

    def list_transcriptions(self):
        names = []
        for hash_dir in os.listdir(f'{self.transcriptions_path}'):
            with self.transcriptions_path.joinpath(hash_dir, Transcription._config_file).open() as fin:
                name = json.load(fin)['name']
                names.append(name)
        return names

