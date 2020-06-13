from pathlib import Path
from typing import Optional

from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.objects.path_structure import PathStructure
from elpis.engines.common.objects.pron_dict import PronDict


class ModelFiles(object):
    def __init__(self, basepath: Path):
        self.kaldi = PathStructure(basepath)


class Model(FSObject):  # TODO not thread safe
    _config_file = 'model.json'
    _links = {**FSObject._links, **{"dataset": Dataset}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset: Optional[Dataset] = None
        self.config['dataset_name'] = None  # dataset hash has not been linked
        self.config['status'] = 'untrained'
        self.status = 'untrained'

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.dataset = None
        return self

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def link(self, dataset: Dataset, pron_dict: PronDict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        self.pron_dict = pron_dict
        self.config['pron_dict_name'] = pron_dict.name
