from pathlib import Path
import sys
from typing import List, Tuple
from elpis.engines.common.input.resample import resample
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.hftransformers.objects.model import FINISHED, UNFINISHED, HFTransformersModel

import soundfile as sf
import torch

from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

LOAD_AUDIO = 'load_audio'
PROCESS_INPUT = 'process_input'
TRANSCRIPTION = 'transcription'
SAVING = 'saving'

STAGES = [
    LOAD_AUDIO,
    PROCESS_INPUT,
    TRANSCRIPTION,
    SAVING
]

FINISHED = 'transcribed'
UNFINISHED = 'transcribing'

class HFTransformersTranscription(BaseTranscription):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Setup paths
        self.audio_file_path = self.path.joinpath("audio.wav")
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.model: HFTransformersModel

        # Setup logging
        run_log_path = self.path.joinpath('train.log')
        sys.stdout = open(run_log_path, 'w')
        sys.stderr = sys.stdout

        stages = { stage: stage for stage in STAGES }
        self.build_stage_status(stages)

    def transcribe(self, on_complete: callable=None) -> None:
        self._set_finished_transcription(False)
        processor, model = self._get_wav2vec2_requirements()

        # Load audio
        self._set_stage(LOAD_AUDIO)
        audio_input, sample_rate = self._load_audio(self.audio_file_path)

        # pad input values and return pt tensor
        self._set_stage(PROCESS_INPUT)
        input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

        # retrieve logits & take argmax
        logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)

        # transcribe
        self._set_stage(TRANSCRIPTION)
        transcription = processor.decode(predicted_ids[0])

        self._set_stage(SAVING)
        self._save_transcription(transcription)

        self._set_finished_transcription(True)
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
        # TODO take transcription and output to a bunch of files.
        print(dir(transcription))

    def _load_audio(self, file: Path) -> Tuple:
        return sf.read(file)

    def prepare_audio(self, audio: Path, on_complete: callable=None):
        self._resample_audio_file(audio, self.audio_file_path)
        if on_complete is not None:
            on_complete()

    def _resample_audio_file(self, audio: Path, dest: Path):
        """Resamples the audio file to be the same sampling rate as the model
        was trained with.

        Target sampling rate is taken from the HFTransformersModel class.

        Parameters:
            audio (Path): A path to a soundfile
            dest (Path): The destination path at which to write the resampled
                    audio.
        """
        data, sample_rate = self._load_audio(audio)

        # Copy to temporary path
        temporary_path = Path(f'/tmp/{self.hash}')
        temporary_path.mkdir(parents=True, exist_ok=True)
        sound_copy = temporary_path.joinpath('original.wav')
        sf.write(sound_copy, data, sample_rate)

        # Resample and overwrite
        sf.write(dest, data, HFTransformersModel.SAMPLING_RATE)

    def _set_finished_transcription(self, has_finished: bool) -> None:
        self.status = FINISHED if has_finished else UNFINISHED

    def _set_stage(self, stage: str) -> None:
        """Updates the stage to one of the constants specified within
        STAGES
        """
        if stage in STAGES:
            self.stage_status = stage, 'starting', ''