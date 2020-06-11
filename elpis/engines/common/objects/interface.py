import json
from shutil import rmtree
from typing import Dict
import os
from abc import abstractmethod
from pathlib import Path

from appdirs import user_data_dir
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.utilities import hasher
from elpis.engines.kaldi.errors import KaldiError
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.pron_dict import PronDict
from elpis.engines.common.objects.model import Model
from elpis.engines.common.objects.transcription import Transcription


class Interface(FSObject):
    _config_file = 'interface.json'
    _data = ['name', 'dataset_name']  # For verbose model listing. NOTE Maybe make a general verbose function for several classes, without need of this variable?
    _classes = {}  # Dict of inherited classes to avoid potential mess in imports. NOTE Need to discuss if it is an adequate pattern.

    def __init__(self, path: Path = None, use_existing=True):
        """
        Constructor for a KaldiInterface object.

        :param path: Path to the object directory on the filesystem.
        :param use_existing: If True and if the object already exists at the
            path, then use the interface object that already exists.
        """

        if path is None:
            name = hasher.new()
            super().__init__(
                parent_path=Path(user_data_dir('elpis')),
                dir_name=name,
                pre_allocated_hash=name,
                name='Kaldi'
            )
        else:
            path = Path(path).absolute()
            # check if already exists
            interface_json_path: Path = path.joinpath('interface.json')
            temp_config = None
            if use_existing and interface_json_path.is_file():
                temp_config = KaldiInterface.load(path).config._load()
            super().__init__(
                parent_path=path.parent,
                dir_name=path.name
            )
            if temp_config is not None:
                self.config._save(temp_config)

        # ensure object directories exist (static sub-paths)
        self.datasets_path: Path = self.path.joinpath('datasets')
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.pron_dicts_path: Path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        self.models_path: Path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        self.transcriptions_path.mkdir(parents=True, exist_ok=True)

        # config objects
        if temp_config is None:
            self.config['datasets'] = {}
            self.config['pron_dicts'] = {}
            self.config['models'] = {}
            self.config['transcriptions'] = {}

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.datasets_path: Path = self.path.joinpath('datasets')
        self.datasets_path.mkdir(parents=True, exist_ok=True)
        self.pron_dicts_path: Path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        self.models_path: Path = self.path.joinpath('models')
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.transcriptions_path = self.path.joinpath('transcriptions')
        self.transcriptions_path.mkdir(parents=True, exist_ok=True)
        return self

    def new_dataset(self, dsname, override=False, use_existing=False):
        """
        Create a new dataset object under this interface.

        :param dsname: String name to assign the dataset.
        :param override: (defualt False) If True then if the name exists, the
            old dataset under that name will be deleted in favor for the new
            name. Cannot be true with the use_existing argument.
        :param use_existing: (default False) If True and a dataset already
            exist with this name, then the dataset returned will be that
            dataset and not a new, blank one. If there is no existing dataset,
            a new one will be created. Cannot be true with the override
            argument.
        :returns: Requested dataset.
        :raises:
            ValueError: if arguments "override" and "use_existing" are both True.
            ValueError: if name already exist without "override" or "use_existing" set to True.
        """
        if override and use_existing:
            raise ValueError('Argguments "override" and "use_existing" cannot both be True at the same time.')
        existing_names = self.list_datasets()
        if dsname in self.config['datasets'].keys():
            if override:
                self.delete_dataset(dsname)
            elif use_existing:
                return self.get_dataset(dsname)
            else:
                raise ValueError(f'data set with name "{dsname}" already exists')
        ds = self._classes["dataset"](parent_path=self.datasets_path, name=dsname)
        datasets = self.config['datasets']
        datasets[dsname] = ds.hash
        self.config['datasets'] = datasets
        return ds
    
    @property
    def state(self):
        raise NotImplementedError()

    def get_dataset(self, dsname):
        if dsname == None:
            return None
        if dsname not in self.list_datasets():
            raise ValueError(f'Tried to load a dataset called "{dsname}" that does not exist')
        hash_dir = self.config['datasets'][dsname]
        return self._classes["dataset"].load(self.datasets_path.joinpath(hash_dir))

    def delete_dataset(self, dsname: str):
        """
        Deletes the dataset with the given name. If the dataset does not
        exist, then nothing is done.

        :param dsname: String name of dataset to delete.
        """
        existing_names = self.list_datasets()
        if dsname in existing_names:
            hash_dir = self.config['datasets'][dsname]
            # Remove the dataset hashed directory
            hash_path: Path = self.datasets_path.joinpath(hash_dir)
            rmtree(hash_path)
            # Remove the dataset (name, hash) entry
            datasets: Dict[str, str] = self.config['datasets']
            datasets.pop(dsname)
            self.config['datasets'] = datasets

    def list_datasets(self):
        names = [name for name in self.config['datasets'].keys()]
        return names

    def new_model(self, mname, override=False, use_existing=False):
        """
        Create a new model object under this interface.

        :param mname: String name to assign the model.
        :param override: (defualt False) If True then if the name exists, the
            old model under that name will be deleted in favor for the new
            name. Cannot be true with the use_existing argument.
        :param use_existing: (default False) If True and a model already
            exist with this name, then the model returned will be that
            model and not a new, blank one. Cannot be true with the override
            argument.
        :returns: Requested model.
        :raises:
            ValueError: if arguments "override" and "use_existing" are both True.
            KaldiError: if name already exist without "override" or "use_existing" set to True.
        """
        if override and use_existing:
            raise ValueError('Argguments "override" and "use_existing" cannot both be True at the same time.')
        existing_names = self.list_datasets()
        if mname in self.config['models'].keys():
            if override:
                self.delete_model(mname)
            elif use_existing:
                return self.get_model(mname)
            else:
                raise KaldiError(
                    f'Tried adding \'{mname}\' which is already in {existing_names} with hash {self.config["models"][mname]}.',
                    human_message=f'model with name "{mname}" already exists'
                )
        m = self._classes["model"](parent_path=self.models_path, name=mname)
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

    def delete_model(self, mname: str):
        """
        Deletes the model with the given name. If the model does not
        exist, then nothing is done.

        :param mname: String name of model to delete.
        """
        existing_names = self.list_models()
        if mname in existing_names:
            hash_dir = self.config['models'][mname]
            # Remove the model hashed directory
            hash_path: Path = self.models_path.joinpath(hash_dir)
            rmtree(hash_path)
            # Remove the model (name, hash) entry
            models: Dict[str, str] = self.config['models']
            models.pop(mname)
            self.config['models'] = models

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

    @abstractmethod
    def new_transcription(self, tname):
        pass

    def get_transcription(self, tname):
        if tname not in self.list_transcriptions():
            raise KaldiError(f'Tried to load a transcription called "{tname}" that does not exist')
        hash_dir = self.config['transcriptions'][tname]
        t = self._classes["transcription"].load(self.transcriptions_path.joinpath(hash_dir))
        t.model = self.get_model(t.config['model_name'])
        return t

    def delete_transcription(self, tname: str):
        """
        Deletes the transcription with the given name. If the transcription does not
        exist, then nothing is done.

        :param tname: String name of transcription to delete.
        """
        existing_names = self.list_transcriptions()
        if tname in existing_names:
            hash_dir = self.config['transcriptions'][tname]
            # Remove the transcription hashed directory
            hash_path: Path = self.transcriptions_path.joinpath(hash_dir)
            rmtree(hash_path)
            # Remove the transcription (name, hash) entry
            transcriptions: Dict[str, str] = self.config['transcriptions']
            transcriptions.pop(tname)
            self.config['transcriptions'] = transcriptions

    def list_transcriptions(self):
        names = []
        for hash_dir in os.listdir(f'{self.transcriptions_path}'):
            if not hash_dir.startswith('.'):
                with self.transcriptions_path.joinpath(hash_dir, self._classes["transcription"]._config_file).open() as fin:
                    name = json.load(fin)['name']
                    names.append(name)
        return names

