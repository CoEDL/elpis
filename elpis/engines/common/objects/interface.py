import json
import os
from pathlib import Path
from shutil import rmtree

from appdirs import user_data_dir
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.utilities import hasher
from elpis.engines.common.utilities.logger import Logger
from elpis.engines.kaldi.errors import KaldiError
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.pron_dict import PronDict


class Interface(FSObject):
    _config_file = 'interface.json'

    def __init__(self, path: Path = None, use_existing=False):
        """
        :param Boolean use_existing: If this flag is enabled and an interface
            already exists at the specified ``path``, then load the interface
            at the ``path``. When ``path`` is not specified or if the
            interface is not at the ``path``, then a new interface is created.
        """
        path_was_none = False
        if path is None:
            path_was_none = True
            name = hasher.new()
            parent_path = Path(user_data_dir('elpis')).joinpath('interfaces')
            path = parent_path.joinpath(name)

            # super().__init__(
            #     parent_path=Path(user_data_dir('elpis')),
            #     dir_name=name,
            #     pre_allocated_hash=name,
            #     name=name
            # )
        

        path = Path(path).absolute()

        # === Check if the existing interface is valid ===================
        # If any of the below nested if-statements fail, the existing (if
        #   it exists) interface is not valid. In that case, wipe the
        #   path directory and start a new interface directory.
        class InvalidInterfaceError(Exception):
            pass
        config_file_path = path.joinpath(Interface._config_file)
        try:
            if (use_existing == True
                and path.exists()
                and path.is_dir()
                and config_file_path.exists()
                and config_file_path.is_file()):
                # a valid interface exists. (this is a shallow check)
                    pass
            else:
                raise InvalidInterfaceError
        
        # === Create a new interface object ==============================
        except InvalidInterfaceError:
            # Must wipe the interface and make a new one
            if path.exists():
                rmtree(path)
            super().__init__(
                parent_path=path.parent,
                dir_name=path.name,
                pre_allocated_hash=(path.name if path_was_none else None),
                name=(path.name if path_was_none else None)
            )
            self.config['loggers'] = []
            self.config['datasets'] = {}
            self.config['pron_dicts'] = {}
            self.config['models'] = {}
            self.config['transcriptions'] = {}

        # === Use existing interface object ==============================
        else:
            # Create a new interface without wiping the directory.
            # Uses existing _config_file.
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
        """
        TODO: fix this.
        Setting the config objects here wipes existing objects from the interface file.
        This means the CLI transcription script can't be run seperately from the CLI training script,
        because this is run whenever the KaldiInterface is initialised.
        However, if we don't set them, we get config KeyErrors (see issue #69).
        KI needs a flag to know whether to set these objects or skip initialising them.
        For now, explicitly set them... sorry CLI.
        """

        

        # make a default logger
        self.new_logger(default=True)

        # set during runtime
        self.engine = None

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
                human_message=f'data set with name "{dsname}" already exists'
            )
        ds = Dataset(parent_path=self.datasets_path, name=dsname)
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
        pd = PronDict(parent_path=self.pron_dicts_path, name=pdname)
        pron_dicts = self.config['pron_dicts']
        pron_dicts[pdname] = pd.hash
        self.config['pron_dicts'] = pron_dicts
        return pd

    def get_pron_dict(self, pdname):
        if pdname not in self.list_pron_dicts():
            raise KaldiError(f'Tried to load a pron dict called "{pdname}" that does not exist')
        hash_dir = self.config['pron_dicts'][pdname]
        pd = PronDict.load(self.pron_dicts_path.joinpath(hash_dir))
        print(dir(pd.config))
        pd.dataset = self.get_dataset(pd.config['dataset_name'])
        return pd

    def list_pron_dicts(self):
        names = [name for name in self.config['pron_dicts'].keys()]
        return names

    def list_pron_dicts_verbose(self):
        pron_dicts = []
        names = [name for name in self.config['pron_dicts'].keys()]
        for name in names:
            pd = self.get_pron_dict(name)
            pron_dicts.append({"name": name, "dataset_name": pd.dataset.name})
        return pron_dicts

    def new_model(self, mname):
        if self.engine is None:
            raise RuntimeError("Engine must be set before model creation")
        print("***********************************))!)@)!@()!@)!(!)@@")
        print(self.engine)
        m = self.engine.model(parent_path=self.models_path, name=mname)
        models = self.config['models']
        models[mname] = m.hash
        self.config['models'] = models
        return m

    def get_model(self, mname):
        if mname not in self.list_models():
            raise KaldiError(f'Tried to load a model called "{mname}" that does not exist')
        hash_dir = self.config['models'][mname]
        m = self.engine.model.load(self.models_path.joinpath(hash_dir))
        m.dataset = self.get_dataset(m.config['dataset_name'])
        m.pron_dict = self.get_pron_dict(m.config['pron_dict_name'])
        return m

    def list_models(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir,
                                               self.engine.model._config_file).open() as fin:
                    name = json.load(fin)['name']
                    models.append(name)
        return models

    def list_models_verbose(self):
        models = []
        for hash_dir in os.listdir(f'{self.models_path}'):
            if not hash_dir.startswith('.'):
                with self.models_path.joinpath(hash_dir,
                                               self.engine.model._config_file).open() as fin:
                    data = json.load(fin)
                    model = {
                        'name': data['name'],
                        'dataset_name': data['dataset_name'],
                        'pron_dict_name': data['pron_dict_name']
                    }
                    models.append(model)
        return models

    def new_transcription(self, tname):
        if self.engine is None:
            raise RuntimeError("Engine need to be set prior to transcription")
        t = self.engine.transcription(parent_path=self.transcriptions_path, name=tname)
        transcriptions = self.config['transcriptions']
        transcriptions[tname] = t.hash
        self.config['transcriptions'] = transcriptions
        return t

    def get_transcription(self, tname):
        if tname not in self.list_transcriptions():
            raise KaldiError(f'Tried to load a transcription called "{tname}" that does not exist')
        hash_dir = self.config['transcriptions'][tname]
        t = self.engine.transcription.load(self.transcriptions_path.joinpath(hash_dir))
        t.model = self.get_model(t.config['model_name'])
        return t

    def list_transcriptions(self):
        names = []
        if not Path(f'{self.transcriptions_path}').exists():
            return names # no directory -> no items in list
        for hash_dir in os.listdir(f'{self.transcriptions_path}'):
            if not hash_dir.startswith('.'):
                with self.transcriptions_path.joinpath(
                        hash_dir, self.engine.transcription._config_file).open() as fin:
                    name = json.load(fin)['name']
                    names.append(name)
        return names

    def set_engine(self, engine):
        self.engine = engine

