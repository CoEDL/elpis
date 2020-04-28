from pathlib import Path
from elpis.objects.dataset import Dataset
from elpis.engines.common.objects.fsobject import FSObject
from elpis.objects.path_structure import KaldiPathStructure


class ModelFiles(object):
    def __init__(self, basepath: Path):
        self.kaldi = KaldiPathStructure(basepath)


class Model(FSObject):  # TODO not thread safe
    _config_file = 'model.json'
    _links = {"dataset": Dataset}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset: Dataset = None
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

    def link(self, *link_objects):
        # NOTE It should be easier to use **links (keyword arguments), but it forces the edition of related endpoint file, so wait for now.
        for link_name, link_class in self._links.items():
            link_object = [link_object for link_object in link_objects if link_object.__class__ == link_class][0]  # Do we need assert length = 1 here?
            setattr(self, link_name, link_object)
            self.config[f"{link_name}_name"] = link_object.name
