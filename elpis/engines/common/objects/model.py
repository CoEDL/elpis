from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.objects.path_structure import PathStructure


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
        # TODO check if this is used, all the other things here are config settings
        self.status = 'untrained'
        self.config['engine_name'] = None  # use this to set engine if loading a model later
        self.config['results'] = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.dataset = None
        return self

    @property
    def status(self):
        return self.config['status'] if self.config['status'] else 'pass'

    @property
    def log(self):
        return self.config['log'] if self.config['log'] else 'pass'

    @property
    def stage_status(self):
        return self.config['stage_status'] if self.config['stage_status'] else 'pass'

    @property
    def results(self):
        return self.config['results']

    @status.setter
    def status(self, value: str):
        if value:
            self.config['status'] = value

    @log.setter
    def log(self, value: str):
        if value:
            self.config['log'] = value

    @stage_status.setter
    def stage_status(self, status_info: Tuple[str, str]):
        stage, status = status_info
        stage_status = self.config['stage_status']
        stage_status[stage]['status'] = status
        self.config['stage_status'] = stage_status

    @results.setter
    def results(self, value: str):
        self.config['results'] = value

    @property
    def settings(self) -> Dict[str, Any]:
        return self.config['settings']

    @settings.setter
    def settings(self, value: Dict[str, Any]) -> None:
        print('model set settings', value)
        self.config['settings'] = value

    def build_stage_status(self, stage_names: Dict[str, str]):
        stage_status = {}
        for stage, name in stage_names.items():
            stage_status[stage] = {'name': name, 'status': 'ready'}
        print('built stage status', stage_status)
        self.config['stage_status'] = stage_status

    def link_dataset(self, dataset: Dataset):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
