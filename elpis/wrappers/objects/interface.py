import os
import json
from shutil import rmtree
from typing import Dict
from elpis.wrappers.utilities import hasher
from pathlib import Path
from appdirs import user_data_dir
from elpis.wrappers.objects.errors import KaldiError
from elpis.wrappers.objects.dataset import Dataset
from elpis.wrappers.objects.pron_dict import PronDict
from elpis.wrappers.objects.model import Model
from elpis.wrappers.objects.transcription import Transcription
from elpis.wrappers.objects.fsobject import FSObject


class KaldiInterface(FSObject):
    _config_file = 'interface.json'

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
                dir_name = name,
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
        ds = Dataset(parent_path=self.datasets_path, name=dsname)
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
        return Dataset.load(self.datasets_path.joinpath(hash_dir))

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

    def new_pron_dict(self, pdname, override=False, use_existing=False):
        """
        Create a new pron dict object under this interface.

        :param pdname: String name to assign the pron dict.
        :param override: (defualt False) If True then if the name exists, the
            old pron dict under that name will be deleted in favor for the new
            name. Cannot be true with the use_existing argument.
        :param use_existing: (default False) If True and a pron dict already
            exist with this name, then the pron dict returned will be that
            pron dict and not a new, blank one. Cannot be true with the override
            argument.
        :returns: Requested pron dict.
        :raises:
            ValueError: if arguments "override" and "use_existing" are both True.
            KaldiError: if name already exist without "override" or "use_existing" set to True.
        """
        if override and use_existing:
            raise ValueError('Argguments "override" and "use_existing" cannot both be True at the same time.')
        existing_names = self.list_datasets()
        if pdname in self.config['pron_dicts'].keys():
            if override:
                self.delete_pron_dict(pdname)
            elif use_existing:
                return self.get_pron_dict(pdname)
            else:
                raise ValueError(f'pronunciation dictionary with name "{pdname}" already exists')
        
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
        pd.dataset = self.get_dataset(pd.config['dataset'])
        return pd
    
    def delete_pron_dict(self, pdname: str):
        """
        Deletes the pron dict with the given name. If the pron dict does not
        exist, then nothing is done.

        :param pdname: String name of pron dict to delete.
        """
        existing_names = self.list_pron_dicts()
        if pdname in existing_names:
            hash_dir = self.config['pron_dicts'][pdname]
            # Remove the pron dict hashed directory
            hash_path: Path = self.pron_dicts_path.joinpath(hash_dir)
            rmtree(hash_path)
            # Remove the pron dict (name, hash) entry
            pron_dicts: Dict[str, str] = self.config['pron_dicts']
            pron_dicts.pop(pdname)
            self.config['pron_dicts'] = pron_dicts

    def list_pron_dicts(self):
        names = [name for name in self.config['pron_dicts'].keys()]
        return names

    def list_pron_dicts_verbose(self):
        pron_dicts = []
        names = [name for name in self.config['pron_dicts'].keys()]
        for name in names:
            pd = self.get_pron_dict(name)
            pron_dicts.append({"name":name, "dataset_name":pd.dataset.name })
        return pron_dicts


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

        m = Model(parent_path=self.models_path, name=mname)
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
                    model = {
                        'name': data['name'],
                        'dataset_name': data['dataset_name'],
                        'pron_dict_name': data['pron_dict_name']
                        }
                    models.append(model)
        return models

    def new_transcription(self, tname, override=False, use_existing=False):
        """
        Create a new transcription object under this interface.

        :param tname: String name to assign the transcription.
        :param override: (defualt False) If True then if the name exists, the
            old transcription under that name will be deleted in favor for the new
            name. Cannot be true with the use_existing argument.
        :param use_existing: (default False) If True and a transcription already
            exist with this name, then the transcription returned will be that
            transcription and not a new, blank one. Cannot be true with the override
            argument.
        :returns: Requested transcription.
        :raises:
            ValueError: if arguments "override" and "use_existing" are both True.
            KaldiError: if name already exist without "override" or "use_existing" set to True.
        """
        if override and use_existing:
            raise ValueError('Argguments "override" and "use_existing" cannot both be True at the same time.')
        existing_names = self.list_datasets()
        if tname in self.config['transcriptions'].keys():
            if override:
                self.delete_transcription(tname)
            elif use_existing:
                return self.get_transcription(tname)
            else:
                raise ValueError(f'transcription with name "{tname}" already exists')

        t = Transcription(parent_path=self.transcriptions_path, name=tname)
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
                with self.transcriptions_path.joinpath(hash_dir, Transcription._config_file).open() as fin:
                    name = json.load(fin)['name']
                    names.append(name)
        return names

