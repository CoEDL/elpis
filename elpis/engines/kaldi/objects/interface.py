from pathlib import Path
from shutil import rmtree
from typing import Dict
from elpis.engines.kaldi.errors import KaldiError
from elpis.engines.common.objects.interface import Interface
from elpis.engines.kaldi.objects.pron_dict import KaldiPronDict
from elpis.engines.kaldi.objects.model import KaldiModel
from elpis.engines.kaldi.objects.dataset import KaldiDataset
from elpis.engines.kaldi.objects.transcription import KaldiTranscription


class KaldiInterface(Interface):
    _data = Interface._data + ['pron_dict_name']
    _classes = {**Interface._classes, **{"dataset": KaldiDataset,
                                         "model": KaldiModel,
                                         "transcription": KaldiTranscription,
                                         "pron_dict": KaldiPronDict}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ensure object directories exist
        self.pron_dicts_path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        # config objects
        self.pron_dicts = {}
        """
        TODO: fix this.
        Setting the config objects here wipes existing objects from the interface file.
        This means the CLI transcription script can't be run seperately from the CLI training 
        script, because this is run whenever the KaldiInterface is initialised.
        However, if we don't set them, we get config KeyErrors (see issue #69).
        KI needs a flag to know whether to set these objects or skip initialising them.
        For now, explicitly set them... sorry CLI.
        """
        self.config['pron_dicts'] = {}

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dicts_path = self.path.joinpath('pron_dicts')
        self.pron_dicts_path.mkdir(parents=True, exist_ok=True)
        # config objects
        self.pron_dicts = {}
        return self

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
        
        pd = KaldiPronDict(parent_path=self.pron_dicts_path, name=pdname)
        pron_dicts = self.config['pron_dicts']
        pron_dicts[pdname] = pd.hash
        self.config['pron_dicts'] = pron_dicts
        return pd

    def get_pron_dict(self, pdname):
        if pdname not in self.list_pron_dicts():
            raise KaldiError(f'Tried to load a pron dict called "{pdname}" that does not exist')
        hash_dir = self.config['pron_dicts'][pdname]
        pd = KaldiPronDict.load(self.pron_dicts_path.joinpath(hash_dir))
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
        
        t = KaldiTranscription(parent_path=self.transcriptions_path, name=tname)
        transcriptions = self.config['transcriptions']
        transcriptions[tname] = t.hash
        self.config['transcriptions'] = transcriptions
        return t

    def get_model(self, mname):
        m = super().get_model(mname)
        m.pron_dict = self.get_pron_dict(m.config['pron_dict_name'])
        return m
