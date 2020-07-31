from pathlib import Path
from typing import Optional, Tuple, Dict

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
        self.config['stage_status'] = {}
        self.status = 'untrained'

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.dataset = None
        return self

    @property
    def status(self):
        return self.config['status']

    @property
    def log(self):
        return self.config['log']

    @property
    def stage_status(self):
        return self.config['stage_status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    @log.setter
    def log(self, value: str):
        self.config['log'] = value

    @stage_status.setter
    def stage_status(self, status_info: Tuple[str, str, str]):
        stage, status, message = status_info
        stage_status = self.config['stage_status']
        stage_status[stage]['status'] = status
        stage_status[stage]['message'] = message
        self.config['stage_status'] = stage_status

    def build_stage_status(self, stage_names: Dict[str, str]):
        for stage_file, stage_name in stage_names.items():
            stage_status = self.config['stage_status']
            stage_status.update({stage_file: {'name': stage_name, 'status': 'ready', 'message': ''}})
            self.config['stage_status'] = stage_status

    def link(self, dataset: Dataset, pron_dict: PronDict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        self.pron_dict = pron_dict
        self.config['pron_dict_name'] = pron_dict.name
