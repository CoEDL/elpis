from abc import ABC
from typing import Type

from elpis.engines.common.objects.interface import Interface
from elpis.engines.common.objects.model import Model
from elpis.engines.common.objects.transcription import Transcription
from elpis.engines.kaldi.objects.model import KaldiModel
from elpis.engines.kaldi.objects.transcription import KaldiTranscription
from elpis.engines.hft.objects.model import HFTModel
from elpis.engines.hft.objects.transcription import HFTTranscription

class Engine(ABC):
    def __init__(self, model: Type[Model], transcription: Type[Transcription]):
        self._model = model
        self._transcription = transcription

    @property
    def model(self) -> Type[Model]:
        return self._model

    @property
    def transcription(self) -> Type[Transcription]:
        return self._transcription

    def __str__(self):
        return f"{type(self).__name__} {type(self.model)} {type(self.transcription)}"


class KaldiEngine(Engine):
    def __init__(self):
        super().__init__(KaldiModel, KaldiTranscription)


class HFTEngine(Engine):
    def __init__(self):
        super().__init__(HFTModel, HFTTranscription)


ENGINES = {
    "kaldi": KaldiEngine(),
    "hft": HFTEngine(),
}
