from pathlib import Path
import sys
from typing import List, Tuple
from elpis.engines.common.objects.transcription import Transcription as BaseTranscription
from elpis.engines.hftransformers.objects.model import FINISHED, UNFINISHED, HFTransformersModel

import soundfile as sf
import torch
from itertools import groupby
import pympi
import string

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

# FINISHED = 'transcribed'
# UNFINISHED = 'transcribing'


class HFTransformersTranscription(BaseTranscription):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Setup paths
        self.audio_file_path = self.path.joinpath("audio.wav")
        self.test_labels_path = self.path / "test-labels-path.txt"
        self.text_path = self.path / "one-best-hypothesis.txt"
        self.xml_path = self.path / "transcription.xml"
        self.elan_path = self.path / "transcription.eaf"
        self.model: HFTransformersModel

        # Setup logging
        run_log_path = self.path.joinpath('train.log')
        sys.stdout = open(run_log_path, 'w')
        sys.stderr = sys.stdout

        self.index_prefixed_stages = [f"{i}_{stage}" for (i, stage) in enumerate(STAGES)]
        stage_labels = [string.capwords(stage).replace('_', ' ') for stage in STAGES]

        stage_names = {file: name for (file, name) in zip(self.index_prefixed_stages, stage_labels)}
        self.build_stage_status(stage_names)

    def transcribe(self, on_complete: callable = None) -> None:
        self._set_finished_transcription(False)
        processor, model = self._get_wav2vec2_requirements()

        # Load audio
        self._set_stage(LOAD_AUDIO)
        audio_input, sample_rate = self._load_audio(self.audio_file_path)
        self._set_stage(LOAD_AUDIO, complete=True)

        # pad input values and return pt tensor
        self._set_stage(PROCESS_INPUT)
        input_values = processor(
            audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values
        self._set_stage(PROCESS_INPUT, msg='Processed input values')

        # retrieve logits & take argmax
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        self._set_stage(PROCESS_INPUT, complete=True)

        # transcribe
        self._set_stage(TRANSCRIPTION)
        transcription = processor.decode(predicted_ids[0])
        self._set_stage(TRANSCRIPTION, complete=True)


        self._set_stage(SAVING)
        self._save_transcription(transcription)

        self._set_stage(SAVING, msg='Saved transcription, generating utterances')
        # Utterances to be used creating elan files
        utterances = self._generate_utterances(
            processor, predicted_ids, input_values, transcription, sample_rate)
        self._save_utterances(utterances)

        self._set_stage(SAVING, complete=True)
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

    def _generate_utterances(self,
                            processor: Wav2Vec2Processor,
                            predicted_ids: torch.Tensor,
                            input_values: torch.Tensor,
                            transcription: str,
                            sample_rate: int) -> Tuple[List[str], List[float], List[float]]:
        """Generates a mapping of words to their start and end times from a transcription.

        Parameters:
            processor: The wav2vec2 processor from which we take the tokenizer.
            predicted_ids 
        """
        words = [word for word in transcription.split(' ') if len(word) > 0]
        predicted_ids = predicted_ids[0].tolist()

        # Add times to ids
        duration_sec = input_values.shape[1] / sample_rate

        time_from_index = lambda index: index / len(predicted_ids) * duration_sec
        generate_timestamps = lambda index, token_idx: (time_from_index(index), token_idx)

        ids_with_time = map(generate_timestamps,
                            enumerate(predicted_ids))

        # remove entries which are just "padding" (i.e. no characers are recognized)
        is_not_padding = lambda _, token_idy: token_idy != processor.tokenizer.pad_token_id
        ids_with_time = filter(is_not_padding, ids_with_time)

        # now split the ids into groups of ids where each group represents a word
        is_delimiter = lambda _, token_idz: token_idz == processor.tokenizer.word_delimiter_token_id
        word_groups = groupby(
            ids_with_time, is_delimiter)

        print(list(word_groups), flush=True)

        # Get all the groups not containing delimiters
        split_ids_w_time = [list(group)
                            for key, group in word_groups if not key]

        # make sure that there are the same number of id-groups as words.
        # Otherwise something is wrong
        assert len(split_ids_w_time) == len(words)

        word_start_times = []
        word_end_times = []
        for cur_ids_w_time, _ in zip(split_ids_w_time, words):
            _times = [time for time, _ in cur_ids_w_time]
            word_start_times.append(min(_times))
            word_end_times.append(max(_times))

        return words, word_start_times, word_end_times

    def _save_transcription(self, transcription: str) -> None:
        """Saves a transcription as plaintext"""
        with open(self.text_path, 'w') as output_file:
            output_file.write(transcription)

    def _save_utterances(self, utterances) -> None:
        """Saves Elan output using the pympi library"""
        result = pympi.Elan.Eaf(file_path = self.elan_path, author="elpis")

        tier = 'spk1' # No idea what this is for
        result.add_tier(tier)

        for word, start, end in zip(*utterances):
            result.add_annotation(id_tier=tier, start=start, end=end, value=word)

    def _load_audio(self, file: Path) -> Tuple:
        return sf.read(file)

    def prepare_audio(self, audio: Path, on_complete: callable = None):
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

    def _set_stage(self, stage: str, complete: bool = False, msg: str = '') -> None:
        """Updates the stage to one of the constants specified within
        STAGES
        """
        status = 'completed' if complete else 'in-progress'
        if stage in STAGES:
            index = STAGES.index(stage)
            self.stage = self.index_prefixed_stages[index]
            self.stage_status = self.stage, status, msg
        

