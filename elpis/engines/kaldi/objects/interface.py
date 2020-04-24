from pathlib import Path
from elpis.engines.kaldi.errors import KaldiError
from elpis.objects.interface import Interface
from .pron_dict import PronDict  # Change later for relative import in same folder.
from .model import model_class  # I could also import KaldiModel, it is a style choice (name genericity even in specific file?) to discuss about!


class KaldiInterface(Interface):
    _data = Interface._data + ['pron_dict_name']
    _classes = {**Interface._classes, **{"model": model_class}}

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
        This means the CLI transcription script can't be run seperately from the CLI training script,
        because this is run whenever the KaldiInterface is initialised.
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

    def list_pron_dicts_verbose(self):
        pron_dicts = []
        names = [name for name in self.config['pron_dicts'].keys()]
        for name in names:
            pd = self.get_pron_dict(name)
            pron_dicts.append({"name":name, "dataset_name":pd.dataset.name })
        return pron_dicts

    def get_model(self, mname):
        m = super().get_model(mname)
        m.pron_dict = self.get_pron_dict(m.config['pron_dict_name'])
        return m

interface_class = KaldiInterface
