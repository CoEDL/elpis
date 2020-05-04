from pathlib import Path
from elpis.engines.common.objects.model import Model
from elpis.engines.common.objects.fsobject import FSObject


class Transcription(FSObject):
    _config_file = "transcription.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None
        self.config["model_name"] = None
        self.config["status"] = "ready"
        self.status = "ready"
        self.type = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.model = None
        return self

    def link(self, model: Model):
        self.model = model
        self.config['model_name'] = model.name

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def text(self):
        pass

    def elan(self):
        pass
