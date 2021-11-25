""" Support for training Hugging Face Transformers (wav2vec2) models."""
import json
import logging
from pathlib import Path
import os
import random
import re
import sys
import time
import string
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Optional, Union, Callable

from elpis.engines.common.objects.command import run
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.model import Model as BaseModel

import datasets
import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torchaudio
from packaging import version
from torch import nn
from torch.utils.tensorboard import SummaryWriter

# import transformers
from transformers import (
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    Wav2Vec2CTCTokenizer,
    Wav2Vec2FeatureExtractor,
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
    is_apex_available,
    set_seed,
)
from transformers.trainer_utils import get_last_checkpoint, is_main_process

if is_apex_available():
    from apex import amp

if version.parse(torch.__version__) >= version.parse("1.6"):
    _is_native_amp_available = True
    from torch.cuda.amp import autocast

logger = logging.getLogger(__name__)

def list_field(default=None, metadata=None):
    return field(default_factory=lambda: default, metadata=metadata)

# Used to reduce training time when debugging
DEBUG = True
QUICK_TRAIN_BUILD_ARGUMENTS = {
    "max_train_samples": 2,
    "num_train_epochs": 1,
    "model_name_or_path": "facebook/wav2vec2-base",
    "per_device_train_batch_size": 1,
    "per_device_eval_batch_size": 1
}

# TODO get this from a GUI model setting
WORD_DELIMITER_TOKEN = " "
NUM_TRAIN_EPOCHS = 10
MINIMUM_DURATION = 0

# Training Stages
TOKENIZATION = "tokenization"
PREPROCESSING = "dataset_preprocessing"
TRAIN = "train"
EVALUATION = "evaluation"

TRAINING_STAGES = [
    TOKENIZATION,
    PREPROCESSING,
    TRAIN,
    EVALUATION
]

UNFINISHED = "untrained"
FINISHED = "trained"

# Use Mixed precision training
FP16 = True if torch.cuda.is_available() else False

class HFTransformersModel(BaseModel):

    OUTPUT_DIR_NAME = "wav2vec2"
    SAMPLING_RATE = 16_000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # HFT does not use a pronunciation dictionary so this will not change from None.
        self.pron_dict = None
        self.config['pron_dict_name'] = None
        # HFT doesn't use an n-gram language model, so this will not change from None.
        self.config['ngram'] = None
        self.config['engine_name'] = "hftransformers"
        self.config['status'] = "untrained"

        # Setup arguments
        self.set_arguments()

        # Setup logging
        # self.run_log_path = self.path.joinpath('train.log')
        # sys.stdout = open(self.run_log_path, 'w')
        sys.stderr = sys.stdout

        # Setup stage names
        self.index_prefixed_stages = [f"{i}_{stage}" for (i, stage) in enumerate(TRAINING_STAGES)]
        stage_labels = [string.capwords(stage).replace('_', ' ') for stage in TRAINING_STAGES]

        stage_names = {file: name for (file, name) in zip(self.index_prefixed_stages, stage_labels)}
        super().build_stage_status(stage_names)

        self._set_stage(TOKENIZATION)


    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dict = None
        return self

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def has_been_trained(self):
        return self.status == "trained"

    def link_dataset(self, dataset: Dataset):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        # Note the _pron_dict is ignored as it's irrelevant to HFT.

    def build_structure(self):
        print("BUILD STRUCTURE")
        # All the file building is done in the initial steps of train().
        # Could move that here, but for now let's leave it as is.

    def set_arguments(self):
        self.model_args = {
            "model_name_or_path": "facebook/wav2vec2-large-xlsr-53",
            "gradient_checkpointing": True,
            "freeze_feature_extractor": True,
            "ctc_loss_reduction": "mean",
            "ctc_zero_infinity": True,
        }
        self.data_args = {
            "train_size": 0.8,
            "split_seed": 42,
            "max_train_samples": None,
            "preprocessing_num_workers": None,
        }
        self.training_args = {
            "output_dir": self.path.joinpath(self.OUTPUT_DIR_NAME),
            "overwrite_output_dir": True,
            "num_train_epochs": NUM_TRAIN_EPOCHS,
            "per_device_train_batch_size": 4,
            "per_device_eval_batch_size": 4,
            "gradient_accumulation_steps": 2,
            "fp16": FP16,
            "do_train": True,
            "do_eval": True,
            "local_rank": -1,
            "n_gpu": 1,
            "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            "seed": 42,
        }

        additional_args = {}
        if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
            with open(sys.argv[1]) as json_file:
                additional_args = json.load(json_file)
        else:
            if DEBUG:
                additional_args = QUICK_TRAIN_BUILD_ARGUMENTS
        for key, value in additional_args.items():
            if key in self.model_args.keys():
                self.model_args[key] = value
            if key in self.data_args.keys():
                self.data_args[key] = value
            if key in self.training_args.keys():
                self.training_args[key] = value

    def get_last_checkpoint(self):
        """
        Detect last checkpoint.
        """
        last_checkpoint = None
        if os.path.isdir(self.training_args["output_dir"]) and self.training_args["do_train"] and not self.training_args["overwrite_output_dir"]:
            last_checkpoint = get_last_checkpoint(self.training_args["output_dir"])
            if last_checkpoint is None and len(os.listdir(self.training_args["output_dir"])) > 0:
                raise ValueError(
                    f"Output directory ({self.training_args['output_dir']}) already exists and is not empty. "
                    "Use --overwrite_output_dir to overcome.")
            elif last_checkpoint is not None:
                logger.info(
                    f"Checkpoint detected, resuming training at {last_checkpoint}. To avoid this behavior, change "
                    "the `--output_dir` or add `--overwrite_output_dir` to train from scratch.")
        return last_checkpoint

    def setup_logging(self):
        """
        Setup logging.
        """
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)],)
        logger.setLevel(logging.INFO if is_main_process(self.training_args["local_rank"]) else logging.WARN)

        # Log on each process the small summary:
        logger.warning(
            f"Process rank: {self.training_args['local_rank']}, device: {self.training_args['device']}, n_gpu: {self.training_args['n_gpu']}"
            + f"distributed training: {bool(self.training_args['local_rank'] != -1)}, 16-bits training: {self.training_args['fp16']}")
        # Set the verbosity to info of the Transformers logger (on main process only):
        # if is_main_process(training_args.local_rank):
        #     transformers.utils.logging.set_verbosity_info()
        logger.info("Training/evaluation parameters %s", self.training_args)

    def get_language_data(self, data_dir, language_file="language_data.json"):
        # Use a json config file to prepare tokens.
        # It is a simple json file with 2 flat lists (graphemes and removables).
        # For now, this must be manually added to the /elpis dir.
        # TODO add a GUI widget for this
        language_data_path = Path(".").joinpath(language_file)
        if language_data_path.exists():
            with open(language_data_path) as fd:
                language_data = json.load(fd)
            logger.info(f"Language data: {language_data}")
        else:
            language_data = None
        return language_data

    def create_split(self, data_dir):
        """ Create annotations files for the train/dev/test splits. """

        elpis_annotations_fn=(data_dir / 'annotations.json')
        with open(elpis_annotations_fn) as f:
            anno_json = json.load(f)

        train_annos, devtest_annos = train_test_split(anno_json,
                test_size=(1-self.data_args["train_size"]),
                random_state=self.data_args["split_seed"])
        if DEBUG:
            train_annos = train_annos[:200]
            devtest_annos = devtest_annos[:60]
        #dev_annos, test_annos = train_test_split(devtest_annos, test_size=0.5, random_state=data_args.split_seed)
        dev_annos = test_annos = devtest_annos


        split_dir = data_dir / 'splits'
        split_dir.mkdir(exist_ok=True)

        with open(split_dir / 'train.json', 'w') as f:
            json.dump({'data': train_annos}, f)
        with open(split_dir / 'dev.json', 'w') as f:
            json.dump({'data': dev_annos}, f)
        with open(split_dir / 'test.json', 'w') as f:
            json.dump({'data': test_annos}, f)

    def get_dataset(self, data_dir):
        split_dir = data_dir / 'splits'
        ds = datasets.load_dataset('json',
                                data_files={'train': str(split_dir / 'train.json'),
                                            'dev': str(split_dir /'dev.json'),
                                            'test': str(split_dir / 'test.json')},
                                field='data')

        def make_text_col(batch):
            batch["text"] = batch['transcript']
            batch["path"] = str(data_dir / 'resampled' / batch['audio_file_name'])
            return batch
        ds = ds.map(make_text_col, remove_columns=['transcript', 'audio_file_name'])
        return ds

    def get_tokenizer(self, data_dir, dataset, word_delimiter_token=WORD_DELIMITER_TOKEN):
        file_name = self.create_vocabulary(data_dir, dataset, word_delimiter_token)

        tokenizer = Wav2Vec2CTCTokenizer(file_name, unk_token='[UNK]', pad_token='[PAD]', word_delimiter_token=word_delimiter_token,)
        return tokenizer

    def create_vocabulary(self, data_dir, dataset, word_delimiter_token, file_name="vocab.json"):
        language_data = self.get_language_data(data_dir)

        def extract_all_chars(batch):
            all_text = " ".join(batch["text"])
            vocab = list(set(all_text))
            return {"vocab": [vocab], "all_text": [all_text]}

        vocab = dataset['train'].map(
            extract_all_chars,
            batched=True,
            batch_size=-1,
            keep_in_memory=True,
            remove_columns=dataset['train'].column_names,)
        vocab_list = list(set(vocab["vocab"][0]))
        naive_vocab_dict = {v: k for k, v in enumerate(vocab_list)}
        if language_data:
            if language_data.get("graphemes"):
                intelligent_vocab_dict = {}
                data_grapheme_duplications = set()
                for token in sorted(language_data["graphemes"], key=len):
                    if token not in intelligent_vocab_dict:
                        intelligent_vocab_dict[token] = len(intelligent_vocab_dict)
                    else:
                        data_grapheme_duplications.add(token)
                if data_grapheme_duplications:
                    logger.warning(f"""Characters duplicated ({len(data_grapheme_duplications)}) in language data: {" ".join(sorted(data_grapheme_duplications))}; duplications were ignored (please clean the data file)…""")
                naive_vocab_set = set(naive_vocab_dict)
                intelligent_vocab_set = set("".join(intelligent_vocab_dict))
                naive_specific_chars = naive_vocab_set - intelligent_vocab_set
                intelligent_specific_chars = intelligent_vocab_set - naive_vocab_set
                if naive_specific_chars:
                    for character in naive_specific_chars:
                        intelligent_vocab_dict[character] = len(intelligent_vocab_dict)
                        logger.warning(f"""Characters present ({len(naive_specific_chars)}) in data but absent in language data: {" ".join(sorted(naive_specific_chars))}; they were added automatically (please update the data file)…""")
                if intelligent_specific_chars:
                    logger.warning(f"""Characters present ({len(intelligent_specific_chars)}) in language data but absent in data: {" ".join(sorted(intelligent_specific_chars))}""")
                vocab_dict = intelligent_vocab_dict
        else:
            vocab_dict = naive_vocab_dict
        vocab_dict["[UNK]"] = len(vocab_dict)
        vocab_dict["[PAD]"] = len(vocab_dict)
        if word_delimiter_token in vocab_dict:
            logging.error(f"The word delimiter token ({word_delimiter_token}) seems to be already present in the raw text, please choose another one.")
        if word_delimiter_token != " " and " " in vocab_dict:
            vocab_dict[word_delimiter_token] = vocab_dict.get(" ", len(vocab_dict))
            del vocab_dict[" "]
        with open(file_name, "w") as vocab_file:
            json.dump(vocab_dict, vocab_file, ensure_ascii=False)
        return file_name

    """
    def tokenize(self, data_args, train_dataset, eval_dataset):
        # Create and save tokenizer
        chars_to_ignore_regex = f'[{"".join(data_args.chars_to_ignore)}]'

        # Is there a better way than doing a nested function here?
        def remove_special_characters(batch):
            batch["text"] = re.sub(chars_to_ignore_regex, "", batch["sentence"]).lower() + " "
            return batch

        train_dataset = train_dataset.map(remove_special_characters, remove_columns=["sentence"])
        eval_dataset = eval_dataset.map(remove_special_characters, remove_columns=["sentence"])
    """

    def get_feature_extractor(self):
        return Wav2Vec2FeatureExtractor(
            feature_size=1, 
            sampling_rate=HFTransformersModel.SAMPLING_RATE, 
            padding_value=0.0, 
            do_normalize=True, 
            return_attention_mask=True)

    def get_processor(self, feature_extractor, tokenizer):
        return Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)

    def get_model(self, processor):
        return Wav2Vec2ForCTC.from_pretrained(
            self.model_args['model_name_or_path'],
            gradient_checkpointing=self.model_args['gradient_checkpointing'],
            ctc_loss_reduction=self.model_args['ctc_loss_reduction'],
            pad_token_id=processor.tokenizer.pad_token_id,
            vocab_size=len(processor.tokenizer),
            ctc_zero_infinity=True)

    def preprocess_dataset(self, dataset):
        speech = self.prepare_speech(dataset)

        def speech_file_to_array_fn(batch):
            #speech_array, sampling_rate = torchaudio.load(batch["path"])
            #process = psutil.Process(os.getpid())
            #print(process.memory_info().rss)
            batch["sampling_rate"] = HFTransformersModel.SAMPLING_RATE
            batch["speech"] = speech[batch['path']][int((batch['start_ms']/1000)*batch['sampling_rate']):int((batch['stop_ms']/1000)*batch['sampling_rate'])]
            batch["target_text"] = batch["text"]
            batch['duration'] = (batch['stop_ms'] - batch['start_ms'])/1000
            batch['duration'] = len(batch['speech'])/batch['sampling_rate']
            return batch

        dataset = dataset.map(
            speech_file_to_array_fn,
            remove_columns=dataset['train'].column_names,
            num_proc=self.data_args["preprocessing_num_workers"],
        )
        return dataset

    def prepare_dataset(self, dataset, processor):
        def prepare_dataset(batch):
            # check that all files have the correct sampling rate
            assert (
                len(set(batch["sampling_rate"])) == 1
            ), f"Make sure all inputs have the same sampling rate of {processor.feature_extractor.sampling_rate}."
            batch["input_values"] = processor(batch["speech"], sampling_rate=batch["sampling_rate"][0]).input_values
            # Setup the processor for targets
            with processor.as_target_processor():
                batch["labels"] = processor(batch["target_text"]).input_ids
            return batch

        dataset = dataset.map(
            prepare_dataset,
            remove_columns=dataset['train'].column_names,
            batch_size=self.training_args["per_device_train_batch_size"],
            batched=True,
            num_proc=self.data_args["preprocessing_num_workers"],
        )
        return dataset

    def prepare_speech(self, dataset):
        speech = {}
        audio_paths = set()
        rejected = 0
        for utt in dataset['train']:
            audio_paths.add((utt['path'], utt['text']))
        for utt in dataset['dev']:
            audio_paths.add((utt['path'], utt['text']))
        for utt in dataset['test']:
            audio_paths.add((utt['path'], utt['text']))
        for path, text in audio_paths:
            speech_array, sampling_rate = torchaudio.load(path)
            audio_metadata = torchaudio.info(path)
            duration = speech_array.size(dim=1) / audio_metadata.sample_rate
            # Num frames exceeds number of characters, wav file is not all zeros, and duration exceeds minimum
            if audio_metadata.num_frames >= len(text) and speech_array.count_nonzero() \
                    and duration > MINIMUM_DURATION:
                resampler = torchaudio.transforms.Resample(sampling_rate, 
                        HFTransformersModel.SAMPLING_RATE)
                speech[path] = resampler(speech_array).squeeze().numpy()
            else:
                rejected += 1

        print("Random sample of 10 transcriptions")
        print("\n".join(random.choices([i[1] for i in audio_paths], k=10)))
        print(rejected, "files removed due to number of frames, zero wav or too short")
        return speech

    def get_trainer(self, dataset, processor, model, tb_writer, metric_name="wer"):
        # Metric
        metric = datasets.load_metric(metric_name)

        def compute_metrics(pred):
            pred_logits = pred.predictions
            pred_ids = np.argmax(pred_logits, axis=-1)
            pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id
            pred_str = processor.batch_decode(pred_ids)
            # we do not want to group tokens when computing the metrics
            label_str = processor.batch_decode(pred.label_ids, group_tokens=False)
            time_str = time.strftime('%Y-%m-%d_%H:%M', time.localtime())
            with open(self.training_args["output_dir"] + f'/dev_preds{time_str}.txt', 'w') as f:
                for pred, ref in zip(pred_str, label_str):
                    print('----------------------------------------', file=f)
                    print('HYP:', file=f)
                    print(pred, file=f)
                    print('REF:', file=f)
                    print(ref, file=f)
                    # for tensorboard
                    tb_writer.add_text('pred', pred)
                    tb_writer.add_text('ref', ref)

            metric_result = metric.compute(predictions=pred_str, references=label_str)
            return {metric_name: metric_result}

        # Data collator
        data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)
        # Initialize our Trainer
        trainer = CTCTrainer(
            model=model,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
            train_dataset=dataset['train'] if self.training_args["do_train"] else None,
            eval_dataset=dataset['dev'] if self.training_args["do_eval"] else None,
            tokenizer=processor.feature_extractor,
            custom_args=self.training_args
        )
        trainer.tb_writer = tb_writer
        return trainer

    def pretrain(self):
        tb_writer = SummaryWriter(self.path / 'runs')

        self.setup_logging()

        set_seed(self.training_args["seed"])

        # 1. Tokenization
        print('Tokenizing...')
        self._set_finished_training(False)
        self._set_stage(TOKENIZATION)

        # Assume dataset has already been linked
        data_dir = Path(self.dataset.pathto.basepath.as_posix())
        self.create_split(data_dir)
        dataset = self.get_dataset(data_dir)

        logging.info('Got dataset.')

        # Load pretrained model and tokenizer
        #
        # Distributed training:
        # The .from_pretrained methods guarantee that only one local process can concurrently
        # download model & vocab.

        logger.info(f'Running on device: {self.training_args["device"]}.')
        print(f'Running on device: {self.training_args["device"]}.')

        tokenizer = self.get_tokenizer(data_dir, dataset)
        feature_extractor = self.get_feature_extractor()
        processor = self.get_processor(feature_extractor, tokenizer)
        model = self.get_model(processor)
        model.to(self.training_args["device"])

        self._set_stage(TOKENIZATION, complete=True)

        # 2. Preprocessing the datasets.
        # We need to read the audio files as arrays and tokenize the targets.
        print('Preprocessing the dataset.')
        self._set_stage(PREPROCESSING)
        dataset = self.preprocess_dataset(dataset)
        dataset = self.prepare_dataset(dataset, processor)

        if self.model_args["freeze_feature_extractor"]:
            model.freeze_feature_extractor()
        
        self._set_stage(PREPROCESSING, complete=True)

        print(f"len of dataset: {len(dataset)}")
        
        # Here to allow for interaction between pretraining and training
        self.dataset = dataset
        self.model = model
        self.processor = processor
        self.tb_writer = tb_writer

    def train(self, on_complete:Callable=None):
        # 3. Training
        self._set_stage(TRAIN)
        trainer = self.get_trainer(self.dataset, self.processor, self.model, self.tb_writer)
        last_checkpoint = self.get_last_checkpoint()
        if self.training_args["do_train"]:
            # Update Checkpoint
            if last_checkpoint is not None:
                checkpoint = last_checkpoint
            elif os.path.isdir(self.model_args["model_name_or_path"]):
                checkpoint = self.model_args["model_name_or_path"]
            else:
                checkpoint = None
            # Train
            train_result = trainer.train(resume_from_checkpoint=checkpoint)
            trainer.save_model()

            # save the feature_extractor and the tokenizer
            if is_main_process(self.training_args["local_rank"]):
                self.processor.save_pretrained(self.training_args["output_dir"])

            metrics = train_result.metrics
            max_train_samples = (
                self.data_args['max_train_samples'] if self.data_args['max_train_samples'] is not None else len(self.dataset['train'])
            )
            metrics["train_samples"] = min(max_train_samples, len(self.dataset['train']))

            trainer.log_metrics(TRAIN, metrics)
            trainer.save_metrics(TRAIN, metrics)
            trainer.save_state()

        self._set_stage(TRAIN, complete=True)
        
        # 4. Evaluation
        self._set_stage(EVALUATION)
        results = {}
        if self.training_args["do_eval"]:
            logger.info("*** Evaluate ***")
            metrics = trainer.evaluate()
            max_val_samples = self.data_args['max_train_samples'] if self.data_args['max_train_samples'] is not None else len(self.dataset['dev'])
            metrics["eval_samples"] = min(max_val_samples, len(self.dataset['dev']))

            trainer.log_metrics("eval", metrics)
            trainer.save_metrics("eval", metrics)
            print("*** metrics")
            print(metrics)
        
        self._set_stage(EVALUATION, complete=True)
        self._set_finished_training(True)
        return results

    def _set_finished_training(self, has_finished: bool) -> None:
        self.status = FINISHED if has_finished else UNFINISHED

    def _set_stage(self, stage: str, complete=False) -> None:
        """Updates the training stage to one of the constants specified within
        TRAINING_STAGES
        """
        if stage not in TRAINING_STAGES:
            return
        status = "completed" if complete else "in-progress"
        index = TRAINING_STAGES.index(stage)
        self.stage = self.index_prefixed_stages[index]
        self.stage_status = self.stage, status, '', ''

    def get_train_results(self) -> Dict[str, float]:
        # TODO Ask Ben what's meant to go here
        return { "comparison_val": 6.9 }
    

class ElpisTokenizer(Wav2Vec2CTCTokenizer):
    """
    Constructs an ElpisTokenizer tokenizer.

    This tokenizer inherits from :class:`~transformers.Wav2Vec2CTCTokenizer` which contains some of the main methods.
    Users should refer to the superclass for more information regarding such methods.
    The specificity of this specialized tokenizer is to manage complexe graphemes (when phonemes are coded on multiple characters) the same way as simple graphemes (see https://github.com/huggingface/transformers/issues/10942).
    It was then managed in a different way by an official PR on the main repository (https://github.com/huggingface/transformers/pull/11349) but I keep for the moment this method based on regular expressions because I prefer semantically not to manage complex graphemes in the same way as "special tokens".
    We should later test their method (and update our fork) to verify that everything works similarly.

    Args:
        vocab_file (:obj:`str`):
            File containing the vocabulary.
        bos_token (:obj:`str`, `optional`, defaults to :obj:`"<s>"`):
            The beginning of sentence token.
        eos_token (:obj:`str`, `optional`, defaults to :obj:`"</s>"`):
            The end of sentence token.
        unk_token (:obj:`str`, `optional`, defaults to :obj:`"<unk>"`):
            The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this
            token instead.
        pad_token (:obj:`str`, `optional`, defaults to :obj:`"<pad>"`):
            The token used for padding, for example when batching sequences of different lengths.
        word_delimiter_token (:obj:`str`, `optional`, defaults to :obj:`"|"`):
            The token used for defining the end of a word.
        do_lower_case (:obj:`bool`, `optional`, defaults to :obj:`False`):
            Whether or not to accept lowercase input and lowercase the output when decoding.

        **kwargs
            Additional keyword arguments passed along to :class:`~transformers.PreTrainedTokenizer`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Characters which will disrupt the regex pattern business
        self.special_characters = ["?", "+", "*", "(", ")", "[", "]", "|"]
        self.pattern: re.Pattern = self.get_pattern()

    def get_pattern(self) -> re.Pattern:
        exclusion_pattern = "|".join([self.unk_token, self.bos_token, self.eos_token, self.pad_token])
        exclusion_pattern = re.sub(r"(\[|/)", r"\\\g<1>", exclusion_pattern)
        # logger.info(f"tokenizer – exclusion pattern: {exclusion_pattern}")
        graphemes = [key if key not in self.special_characters else f"\{key}" for key in self.encoder.keys() if
                     not re.match(exclusion_pattern, key, re.I)]
        logger.info(f"tokenizer – graphemes: {graphemes}")
        pattern = re.compile("|".join(sorted(graphemes, key=lambda grapheme: len(grapheme), reverse=True)))
        logger.info(f"tokenizer – tokenization pattern: {pattern}")
        return pattern

    def _tokenize(self, text: str) -> List[str]:
        """
        Converts a string in a sequence of tokens (string), using the tokenizer.
        """
        if self.do_lower_case:
            text = text.upper()
        tokens = re.findall(self.pattern, text)
        # logger.info(f"tokenizer – tokens: {text} → {tokens}")
        return tokens

    #############################################
    # Not sure if it is useful yet (the tokenizer function, later, will create a pattern with longest graphemes before the shortest ones, but maybe some linguists won’t give the graphemes in an classified way and this function could be useful for printing data or whatever…
    def classify_graphemes(graphemes: Union[List[str], Set[str]], by: Callable = len) -> Dict[int, List[str]]:
        """
        Returns a dict where keys are the criteria results of a function applied on graphemes, and values lists of graphemes under this criteria (length by default).
        """
        grapheme_dict = {}
        for grapheme in graphemes:
            grapheme_list = grapheme_dict.get(by(grapheme), [])
            grapheme_list.append(grapheme)
            grapheme_dict[by(grapheme)] = grapheme_list
        return grapheme_dict

@dataclass
class DataCollatorCTCWithPadding:
    """
    Data collator that will dynamically pad the inputs received.
    Args:
        processor (:class:`~transformers.Wav2Vec2Processor`)
            The processor used for proccessing the data.
        padding (:obj:`bool`, :obj:`str` or :class:`~transformers.tokenization_utils_base.PaddingStrategy`, `optional`, defaults to :obj:`True`):
            Select a strategy to pad the returned sequences (according to the model's padding side and padding index)
            among:
            * :obj:`True` or :obj:`'longest'`: Pad to the longest sequence in the batch (or no padding if only a single
              sequence if provided).
            * :obj:`'max_length'`: Pad to a maximum length specified with the argument :obj:`max_length` or to the
              maximum acceptable input length for the model if that argument is not provided.
            * :obj:`False` or :obj:`'do_not_pad'` (default): No padding (i.e., can output a batch with sequences of
              different lengths).
        max_length (:obj:`int`, `optional`):
            Maximum length of the ``input_values`` of the returned list and optionally padding length (see above).
        max_length_labels (:obj:`int`, `optional`):
            Maximum length of the ``labels`` returned list and optionally padding length (see above).
        pad_to_multiple_of (:obj:`int`, `optional`):
            If set will pad the sequence to a multiple of the provided value.
            This is especially useful to enable the use of Tensor Cores on NVIDIA hardware with compute capability >=
            7.5 (Volta).
    """

    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True
    max_length: Optional[int] = None
    max_length_labels: Optional[int] = None
    pad_to_multiple_of: Optional[int] = None
    pad_to_multiple_of_labels: Optional[int] = None

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lenghts and need
        # different padding methods
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors="pt",
        )
        with self.processor.as_target_processor():
            labels_batch = self.processor.pad(
                label_features,
                padding=self.padding,
                max_length=self.max_length_labels,
                pad_to_multiple_of=self.pad_to_multiple_of_labels,
                return_tensors="pt",
            )

        # replace padding with -100 to ignore loss correctly
        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        batch["labels"] = labels

        return batch


class CTCTrainer(Trainer):
    def __init__(self, custom_args, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_args = custom_args
        self.args.seed = custom_args["seed"]

    def training_step(self, model: nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]) -> torch.Tensor:
        """
        Perform a training step on a batch of inputs.

        Subclass and override to inject custom behavior.

        Args:
            model (:obj:`nn.Module`):
                The model to train.
            inputs (:obj:`Dict[str, Union[torch.Tensor, Any]]`):
                The inputs and targets of the model.

                The dictionary will be unpacked before being fed to the model. Most models expect the targets under the
                argument :obj:`labels`. Check your model's documentation for all accepted arguments.

        Return:
            :obj:`torch.Tensor`: The tensor with training loss on this batch.
        """

        model.train()
        inputs = self._prepare_inputs(inputs)

        if self.use_amp:
            with autocast():
                loss = self.compute_loss(model, inputs)
        else:
            loss = self.compute_loss(model, inputs)

        if self.custom_args["n_gpu"] > 1:
            if model.module.config.ctc_loss_reduction == "mean":
                loss = loss.mean()
            elif model.module.config.ctc_loss_reduction == "sum":
                loss = loss.sum() / (inputs["labels"] >= 0).sum()
            else:
                raise ValueError(f"{model.config.ctc_loss_reduction} is not valid. Choose one of ['mean', 'sum']")

        if self.custom_args["gradient_accumulation_steps"] > 1:
            loss = loss / self.custom_args["gradient_accumulation_steps"]

        if self.use_amp:
            self.scaler.scale(loss).backward()
        elif self.use_apex:
            with amp.scale_loss(loss, self.optimizer) as scaled_loss:
                scaled_loss.backward()
        elif self.deepspeed:
            self.deepspeed.backward(loss)
        else:
            loss.backward()

        print(f"\nLoss|epoch {loss} {self.state.epoch}") # tensor(3.9470, device='cuda:0', grad_fn=<DivBackward0>)
        # TODO sum the loss over training steps to get loss per epoch, instead of ben's hacky business below
        # To see what is happening in finer detail, multiply epoch so that eg epoch 0.1 will be logged as 1
        epoch_multiplier = 10
        self.tb_writer.add_scalar('Loss', loss.item(), self.state.epoch * epoch_multiplier)

        return loss.detach()

# For dev test purpose (to run without the GUI)…
if __name__ == "__main__":
    model = HFTransformersModel(parent_path="..")
    model.train()
