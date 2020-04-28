from pathlib import Path
from elpis.engines.common.objects.model import Model
from elpis.engines.common.input.resample import resample
from elpis.engines.common.objects.fsobject import FSObject
import subprocess
from typing import Callable
import os
from distutils import dir_util, file_util
import wave
import contextlib


class Transcription(FSObject):
    _config_file = "transcription.json"
    _links = {"model": Model}

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

    def link(self, *link_objects):
        # NOTE See comment for same function in model.py. NOTE Maybe to move to FSObject generic function?
        for link_name, link_class in self._links.items():
            link_object = [link_object for link_object in link_objects if issubclass(link_object.__class__, link_class)][0]  # Do we need assert length = 1 here?
            setattr(self, link_name, link_object)
            self.config[f"{link_name}_name"] = link_object.name

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