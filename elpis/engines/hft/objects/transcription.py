import string
import sys
from itertools import groupby
from pathlib import Path
from pprint import pprint
from typing import List, Tuple
from enum import Enum

import pympi
import torch
from loguru import logger
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
from werkzeug.datastructures import FileStorage

import elpis.engines.common.utilities.resampling as resampler
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.hft.objects.model import HFTModel


STAGES = Enum("STAGES_ENUM", "load_model load_audio transcription saving")
TRANSCRIPTION_STATUS = Enum("TRANSCRIPTION_STATUS", "transcribed transcribing")


class HFTTranscription(BaseTranscription):

    SAMPLING_RATE = 16_000

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Setup paths
        self.audio_filename = None
        self.audio_file_path = None
        self.test_labels_path = self.path / "test-labels-path.txt"
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.model: HFTModel

        self.index_prefixed_stages = [f"{i}_{stage.name}" for (i, stage) in enumerate(STAGES)]
        stage_labels = [string.capwords(stage.name).replace("_", " ") for stage in STAGES]

        stage_names = {file: name for (file, name) in zip(self.index_prefixed_stages, stage_labels)}
        self.build_stage_status(stage_names)

    def transcribe(self, on_complete: callable = None) -> None:
        self._set_stage(STAGES.load_model.name)
        logger.info("=== Load model ===")
        self._set_finished_transcription(False)
        processor, model = self._get_wav2vec2_requirements()
        self._set_stage(STAGES.load_model.name, complete=True)

        # TODO move to GPU if available

        self._set_stage(STAGES.load_audio.name)
        logger.info("=== Load audio ===")
        audio_input, _ = resampler.load_audio(
            self.audio_file_path, target_sample_rate=HFTTranscription.SAMPLING_RATE
        )
        self._set_stage(STAGES.load_audio.name, complete=True)

        self._set_stage(STAGES.transcription.name)
        logger.info("=== Inference pipeline ===")

        # Use GPU if available. -1 is CPU
        device = "0" if torch.cuda.is_available() else "-1"

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            device=device
        )
        transcription = pipe(audio_input, chunk_length_s=10, return_timestamps="word")
        logger.info(transcription["text"])
        self._set_stage(STAGES.transcription.name, complete=True)

        self._set_stage(STAGES.saving.name, msg="Saving transcription text")
        logger.info("=== Save transcription text ===")
        self._save_transcription(transcription["text"])

        self._set_stage(STAGES.saving.name, msg="Saving utterances in Elan format")
        logger.info("=== Save utterances in Elan format ===")
        self._save_utterances(transcription["chunks"])

        self._set_stage(STAGES.saving.name, complete=True)
        self._set_finished_transcription(True)

        # TODO move model off GPU

        if on_complete is not None:
            on_complete()

    def text(self):
        with open(self.text_path, "r") as text_file:
            text = text_file.read()
            return text

    def elan(self):
        with open(self.elan_path, "r") as elan_file:
            return elan_file.read()

    def get_confidence(self):
        return None

    def _get_wav2vec2_requirements(self) -> Tuple[Wav2Vec2Processor, Wav2Vec2ForCTC]:
        """
        Builds and returns pretrained Wav2Vec2 Processor and Model from the project path.
        """
        pretrained_path = self.model.output_dir
        logger.info(f"Loading processor from {pretrained_path}")
        processor = Wav2Vec2Processor.from_pretrained(pretrained_path)
        logger.info(f"Loading model from {pretrained_path}")
        model = Wav2Vec2ForCTC.from_pretrained(pretrained_path)
        logger.info(f"Returning processor and model from {pretrained_path}")
        return processor, model

    def _save_transcription(self, transcription: str) -> None:
        """
        Saves a transcription as plaintext
        """
        with open(self.text_path, "w") as output_file:
            output_file.write(transcription)

    def _save_utterances(self, utterances) -> None:
        """
        Saves Elan output using the pympi library
        """
        result = pympi.Elan.Eaf(author="elpis")
        result.add_linked_file(self.audio_filename)
        result.add_tier("default")
        to_millis = lambda seconds: int(seconds * 1000)
        for utterance in utterances:
            word = utterance["text"]
            start, end = (
                to_millis(utterance["timestamp"][0]),
                to_millis(utterance["timestamp"][1]) + 1,
            )
            result.add_annotation(id_tier="default", start=start, end=end, value=word)
        pympi.Elan.to_eaf(self.elan_path, result)

    def prepare_audio(self, audio: FileStorage, on_complete: callable = None):
        logger.info(f"=== Prepare audio for transcription {audio} ===")
        self.audio_filename = audio.filename
        self.audio_file_path = self.path.joinpath(self.audio_filename)

        resampler.resample_from_file_storage(audio, self.audio_file_path, HFTModel.SAMPLING_RATE)
        if on_complete is not None:
            on_complete()

    def _set_finished_transcription(self, has_finished: bool) -> None:
        self.status = (
            TRANSCRIPTION_STATUS.transcribed.name
            if has_finished
            else TRANSCRIPTION_STATUS.transcribing.name
        )

    def _set_stage(self, stage: str, complete: bool = False, msg: str = "") -> None:
        """
        Updates the stage status for display in the GUI.
        self.stage combines the stage index (for ease of sorting in the GUI) with the stage name, eg 0_load_model
        """
        status = "complete" if complete else "in-progress"

        for (i, stage_) in enumerate(STAGES):
            if stage == stage_.name:
                self.stage = self.index_prefixed_stages[i]
                self.stage_status = self.stage, status, msg
