from pathlib import Path
from typing import List, Tuple
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.hftransformers.objects.model import HFTransformersModel

import soundfile as sf
import torch

from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

class HFTransformersTranscription(BaseTranscription):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Setup paths
        self.audio_file_path = self.path.joinpath("audio.wav")
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.model: HFTransformersModel

    def transcribe(self, on_complete: callable=None) -> None:
        self.status = "transcribing"
        processor, model = self._get_wav2vec2_requirements()

        # Load audio
        audio_input, sample_rate = self._load_audio(self.audio_file_path)

        # pad input values and return pt tensor
        input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

        # retrieve logits & take argmax
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)

        # transcribe
        transcription = processor.decode(predicted_ids[0])
        self._save_transcription(transcription)

        self.status = "transcribed"
        if on_complete is not None:
            on_complete()
    
    def text(self):
        with open(self.text_path, 'r') as fin:
            text = fin.read()
            return text

    def elan(self):
        with open(self.elan_path, 'r') as fin:
            return fin.read()

    def _get_wav2vec2_requirements(self) -> Tuple[Wav2Vec2Processor, Wav2Vec2ForCTC]:
        """Builds and returns pretrained Wav2Vec2 Processor and Model from the
        project path.
        """
        pretrained_path = Path(self.model.path) / self.model.OUTPUT_DIR_NAME

        processor = Wav2Vec2Processor.from_pretrained(pretrained_path)
        model = Wav2Vec2ForCTC.from_pretrained(pretrained_path)
        
        return processor, model

    def _save_transcription(self, transcription: List[str]) -> None:
        """Saves a transcription in a bunch of required formats for future
        processing.
        """
        # TODO
        print(transcription)

    def _load_audio(self, file) -> Tuple:
        return sf.read(file)

   