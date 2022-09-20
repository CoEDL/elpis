import string
import sys
from itertools import groupby
from pathlib import Path
from pprint import pprint
from typing import List, Tuple

import pympi
import torch
from loguru import logger
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from werkzeug.datastructures import FileStorage

import elpis.engines.common.utilities.resampling as resampler
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.hft.objects.model import HFTModel

LOAD_AUDIO = "load_audio"
PROCESS_INPUT = "process_input"
TRANSCRIPTION = "transcription"
SAVING = "saving"

STAGES = [LOAD_AUDIO, PROCESS_INPUT, TRANSCRIPTION, SAVING]

FINISHED = "transcribed"
UNFINISHED = "transcribing"


class HFTTranscription(BaseTranscription):

    SAMPLING_RATE = 16_000

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Setup paths
        self.audio_file_path = self.path.joinpath("audio.wav")
        self.test_labels_path = self.path / "test-labels-path.txt"
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.model: HFTModel

        self.index_prefixed_stages = [f"{i}_{stage}" for (i, stage) in enumerate(STAGES)]
        stage_labels = [string.capwords(stage).replace("_", " ") for stage in STAGES]

        stage_names = {file: name for (file, name) in zip(self.index_prefixed_stages, stage_labels)}
        self.build_stage_status(stage_names)

    def transcribe(self, on_complete: callable = None) -> None:
        logger.info("==== Load processor and model ====")
        self._set_finished_transcription(False)
        processor, model = self._get_wav2vec2_requirements()

        # Load audio
        self._set_stage(LOAD_AUDIO)
        logger.info("=== Load audio")
        audio_input, _ = resampler.load_audio(
            self.audio_file_path, target_sample_rate=HFTTranscription.SAMPLING_RATE
        )
        self._set_stage(LOAD_AUDIO, complete=True)

        # Pad input values and return pt tensor
        self._set_stage(PROCESS_INPUT)
        logger.info("==== Process input ====")
        input_values = processor(
            audio_input, sampling_rate=HFTTranscription.SAMPLING_RATE, return_tensors="pt"
        ).input_values
        self._set_stage(PROCESS_INPUT, msg="Processed input values")

        # Retrieve logits & take argmax
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        self._set_stage(PROCESS_INPUT, complete=True)

        # Transcribe
        self._set_stage(TRANSCRIPTION)
        transcription = processor.decode(predicted_ids[0])
        logger.info(f"{transcription=}")
        self._set_stage(TRANSCRIPTION, complete=True)

        self._set_stage(SAVING)
        logger.info("==== Save transcription ====")
        self._save_transcription(transcription)

        self._set_stage(SAVING, msg="Saved transcription, generating utterances")
        # Utterances to be used creating elan files
        logger.info("==== Generate utterances ====")
        utterances = self._generate_utterances(
            processor, predicted_ids, input_values, transcription
        )
        logger.info("==== Save utterances (elan and text) ====")
        self._save_utterances(utterances)

        self._set_stage(SAVING, complete=True)
        self._set_finished_transcription(True)
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

    def _generate_utterances(
        self,
        processor: Wav2Vec2Processor,
        predicted_ids: torch.Tensor,
        input_values: torch.Tensor,
        transcription: str,
    ) -> Tuple[List[str], List[float], List[float]]:
        """
        Generates a mapping of words to their start and end times from a transcription.

        Parameters:
            processor: The wav2vec2 processor from which we take the tokenizer.
            predicted_ids: TODO
            input_values: TODO
            transcription: The hypothesis text.
        """
        words = [word for word in transcription.split(" ") if len(word) > 0]
        predicted_ids = predicted_ids[0].tolist()

        # Determine original sample rate
        original_file = resampler.ORIGINAL_SOUND_FILE_DIRECTORY / self.audio_file_path.name
        _, sample_rate = resampler.load_audio(original_file)

        # Add times to ids
        duration_sec = input_values.shape[1] / sample_rate
        logger.info(f"Audio length: {duration_sec}")

        time_from_index = lambda index: index / len(predicted_ids) * duration_sec
        generate_timestamps = lambda item: (time_from_index(item[0]), item[1])

        ids_with_time = map(generate_timestamps, enumerate(predicted_ids))

        # remove entries which are just 'padding' (i.e. no characers are recognized)
        is_not_padding = lambda item: item[1] != processor.tokenizer.pad_token_id
        ids_with_time = filter(is_not_padding, ids_with_time)

        # now split the ids into groups of ids where each group represents a word
        is_delimiter = lambda item: item[1] == processor.tokenizer.word_delimiter_token_id
        word_groups = groupby(ids_with_time, is_delimiter)

        # Get all the groups not containing delimiters
        split_ids_w_time = [list(group) for key, group in word_groups if not key]

        # make sure that there are the same number of id-groups as words.
        # Otherwise something is wrong
        logger.info(f"Length check: {len(split_ids_w_time)} {len(words)}")
        assert len(split_ids_w_time) == len(words)

        word_start_times = []
        word_end_times = []
        for cur_ids_w_time, _ in zip(split_ids_w_time, words):
            _times = [time for time, _ in cur_ids_w_time]
            word_start_times.append(min(_times))
            word_end_times.append(max(_times))

        logger.info(f"{words=}")
        pprint(list(zip(word_start_times, word_end_times)))
        return words, word_start_times, word_end_times

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

        result.add_linked_file("audio.wav")
        result.add_tier("default")

        to_millis = lambda seconds: int(seconds * 1000)
        for word, start, end in zip(*utterances):
            start, end = to_millis(start), to_millis(end) + 1
            result.add_annotation(id_tier="default", start=start, end=end, value=word)

        pympi.Elan.to_eaf(self.elan_path, result)

    def prepare_audio(self, audio: Path, on_complete: callable = None):
        logger.info(f"=== Prepare audio {audio} {self.audio_file_path}")
        resampler.resample_from_file_storage(audio, self.audio_file_path, HFTModel.SAMPLING_RATE)
        if on_complete is not None:
            on_complete()

    def _set_finished_transcription(self, has_finished: bool) -> None:
        self.status = FINISHED if has_finished else UNFINISHED

    def _set_stage(self, stage: str, complete: bool = False, msg: str = "") -> None:
        """
        Updates the stage to one of the constants specified within STAGES
        """
        status = "completed" if complete else "in-progress"
        if stage in STAGES:
            index = STAGES.index(stage)
            self.stage = self.index_prefixed_stages[index]
            self.stage_status = self.stage, status, msg
