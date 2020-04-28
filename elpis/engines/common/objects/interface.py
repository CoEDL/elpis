import os
import json
from elpis.engines.common.utilities import hasher
from pathlib import Path
from appdirs import user_data_dir
from elpis.engines.kaldi.errors import KaldiError
from elpis.engines.common.objects.logger import Logger
from elpis.engines.common.objects.fsobject import FSObject


class Interface(FSObject):
    _config_file = 'interface.json'
    _data = ['name', 'dataset_name']  # For verbose model listing.
    _classes = {}  # Dict of inherited classes to avoid potential mess in imports. NOTE Need to discuss if it is an adequate pattern.

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
        """
        TODO: fix this.
        Setting the config objects here wipes existing objects from the interface file.
        This means the CLI transcription script can't be run seperately from the CLI training script,
        because this is run whenever the Interface is initialised.
        However, if we don't set them, we get config KeyErrors (see issue #69).
        KI needs a flag to know whether to set these objects or skip initialising them.
        For now, explicitly set them... sorry CLI.
        """
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
                human_message=f'data set with name "{dsname}" already exists'
            )
        ds = self._classes["dataset"](parent_path=self.datasets_path, name=dsname, logger=self.logger)
        datasets = self.config['datasets']
        datasets[dsname] = ds.hash
        self.config['datasets'] = datasets
        return ds

    def get_dataset(self, dsname):
        if dsname not in self.list_datasets():
            raise KaldiError(f'Tried to load a dataset called "{dsname}" that does not exist')
        hash_dir = self.config['datasets'][dsname]
        return self._classes["dataset"].load(self.datasets_path.joinpath(hash_dir))

    def list_datasets(self):
        names = [name for name in self.config['datasets'].keys()]
        return names

    def new_model(self, mname):
        m = self._classes["model"](parent_path=self.models_path, name=mname, logger=self.logger)
        models = self.config['models']
        models[mname] = m.hash
        self.config['models'] = models
        return m

    def get_model(self, mname):
        if mname not in self.list_models():
            raise KaldiError(f'Tried to load a model called "{mname}" that does not exist')
        hash_dir = self.config['models'][mname]
        m = self._classes["model"].load(self.models_path.joinpath(hash_dir))
        m.dataset = self.get_dataset(m.config['dataset_name'])
        return m

    def list_models(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir, self._classes["model"]._config_file).open() as fin:
                    name = json.load(fin)['name']
                    models.append(name)
        return models

    def list_models_verbose(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir, self._classes["model"]._config_file).open() as fin:
                    data = json.load(fin)
                    model = {name: data[name] for name in self._data}
                    models.append(model)
        return models

    def new_transcription(self, tname):
        t = self._classes["transcription"](parent_path=self.transcriptions_path, name=tname, logger=self.logger)
        transcriptions = self.config['transcriptions']
        transcriptions[tname] = t.hash
        self.config['transcriptions'] = transcriptions
        return t

    def get_transcription(self, tname):
        if tname not in self.list_transcriptions():
            raise KaldiError(f'Tried to load a transcription called "{tname}" that does not exist')
        hash_dir = self.config['transcriptions'][tname]
        t = self._classes["transcription"].load(self.transcriptions_path.joinpath(hash_dir))
        t.model = self.get_model(t.config['model_name'])
        return t

    def list_transcriptions(self):
        names = []
        for hash_dir in os.listdir(f'{self.transcriptions_path}'):
            if not hash_dir.startswith('.'):
                with self.transcriptions_path.joinpath(hash_dir, self._classes["transcription"]._config_file).open() as fin:
                    name = json.load(fin)['name']
                    names.append(name)
        return names

