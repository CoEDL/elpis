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
    _links = {**FSObject._links, **{"model": Model}}

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