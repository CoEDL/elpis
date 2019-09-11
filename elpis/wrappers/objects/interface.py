import os
import json
from elpis.wrappers.utilities import hasher
from pathlib import Path
from appdirs import user_data_dir
from elpis.wrappers.objects.errors import KaldiError
from elpis.wrappers.objects.dataset import Dataset
from elpis.wrappers.objects.pron_dict import PronDict
from elpis.wrappers.objects.logger import Logger
from elpis.wrappers.objects.model import Model
from elpis.wrappers.objects.transcription import Transcription
from elpis.wrappers.objects.fsobject import FSObject


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
        self.pron_dicts_path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        self.models_path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.loggers_path = self.path.joinpath('loggers')
        self.loggers_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        # config objects
        self.loggers = []
        self.datasets = {}
        self.pron_dicts = {}
        self.models = {}
        self.transcriptions = {}

        self.config['loggers'] = []
        self.config['datasets'] = {}
        self.config['pron_dicts'] = {}
        self.config['models'] = {}
        self.config['transcriptions'] = {}

        # make a default logger
        self.new_logger(default=True)

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.datasets_path = self.path.joinpath('datasets')
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.pron_dicts_path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        self.models_path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.loggers_path = self.path.joinpath('loggers')
        self.loggers_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        # config objects
        self.loggers = []
        self.datasets = {}
        self.pron_dicts = {}
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



    def new_pron_dict(self, pdname):
        pd = PronDict(parent_path=self.pron_dicts_path, name=pdname, logger=self.logger)
        pron_dicts = self.config['pron_dicts']
        pron_dicts[pdname] = pd.hash
        self.config['pron_dicts'] = pron_dicts
        return pd

    def get_pron_dict(self, pdname):
        if pdname not in self.list_pron_dicts():
            raise KaldiError(f'Tried to load a pron dict called "{pdname}" that does not exist')
        hash_dir = self.config['pron_dicts'][pdname]
        pd = PronDict.load(self.pron_dicts_path.joinpath(hash_dir))
        pd.dataset = self.get_dataset(pd.config['dataset_name'])
        return pd

    def list_pron_dicts(self):
        names = [name for name in self.config['pron_dicts'].keys()]
        return names



    def new_model(self, mname):
        m = Model(parent_path=self.models_path, name=mname, logger=self.logger)
        models = self.config['models']
        models[mname] = m.hash
        self.config['models'] = models
        return m

    def get_model(self, mname):
        if mname not in self.list_models():
            raise KaldiError(f'Tried to load a model called "{mname}" that does not exist')
        hash_dir = self.config['models'][mname]
        m = Model.load(self.models_path.joinpath(hash_dir))
        m.dataset = self.get_dataset(m.config['dataset_name'])
        m.pron_dict = self.get_pron_dict(m.config['pron_dict_name'])
        return m

    def list_models(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir, Model._config_file).open() as fin:
                    name = json.load(fin)['name']
                    models.append(name)
        return models

    def list_models_verbose(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir, Model._config_file).open() as fin:
                    data = json.load(fin)
                    model = {'name': data['name'], 'dataset_name': data['dataset_name']}
                    models.append(model)
        return models

    def new_transcription(self, tname):
        t = Transcription(parent_path=self.transcriptions_path, name=tname, logger=self.logger)
        transcriptions = self.config['transcriptions']
        transcriptions[tname] = t.hash
        self.config['transcriptions'] = transcriptions
        return t

    def get_transcription(self, tname):
        if tname not in self.list_transcriptions():
            raise KaldiError(f'Tried to load a transcription called "{tname}" that does not exist')
        hash_dir = self.config['transcriptions'][tname]
        t = Transcription.load(self.transcriptions_path.joinpath(hash_dir))
        t.model = self.get_model(t.config['model_name'])
        return t

    def list_transcriptions(self):
        names = []
        for hash_dir in os.listdir(f'{self.transcriptions_path}'):
            if not hash_dir.startswith('.'):
                with self.transcriptions_path.joinpath(hash_dir, Transcription._config_file).open() as fin:
                    name = json.load(fin)['name']
                    names.append(name)
        return names

