from . import hasher
from pathlib import Path
from .session import Session


class Transcription(object):
    def __init__(self, basepath: Path, name:str, sesson: Session, model):
        super().__init__()
        self.name: str = name
        self.hash: str = hasher.new()
        self.path: Path = basepath.joinpath(self.hash)
        self.path.mkdir(parents=True, exist_ok=True)
        self.model = model
    def transcribe(self, path: Path):
        pass
    def results(self):
        return "no results yet"
