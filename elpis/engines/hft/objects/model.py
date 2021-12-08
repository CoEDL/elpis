"""
Support for training Hugging Face Transformers (wav2vec2) models.
"""
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
from packaging import version

import datasets
import numpy as np
from sklearn.model_selection import train_test_split
import torch
import torchaudio
from torch import nn
from torch.utils.tensorboard import SummaryWriter
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

from elpis.engines.common.objects.command import run
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.model import Model as BaseModel


if is_apex_available():
    from apex import amp

if version.parse(torch.__version__) >= version.parse('1.6'):
    _is_native_amp_available = True
    from torch.cuda.amp import autocast


# Used to reduce training time when debugging
DEBUG = False
QUICK_TRAIN_BUILD_ARGUMENTS = {
    'num_train_epochs': '3',
    'model_name_or_path': 'facebook/wav2vec2-base',
    'per_device_train_batch_size': '1',
    'per_device_eval_batch_size': '1',
}

# Training Stages
TOKENIZATION = 'tokenization'
PREPROCESSING = 'dataset_preprocessing'
TRAIN = 'train'
EVALUATION = 'evaluation'

TRAINING_STAGES = [
    TOKENIZATION,
    PREPROCESSING,
    TRAIN,
    EVALUATION
]

UNFINISHED = 'untrained'
FINISHED = 'trained'

logger = logging.getLogger(__name__)


def list_field(default=None, metadata=None):
    return field(default_factory=lambda: default, metadata=metadata)


class HFTModel(BaseModel):

    SAMPLING_RATE = 16_000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # HFT does not use a pronunciation dictionary so this will not change from None.
        self.pron_dict = None
        self.config['pron_dict_name'] = None
        # HFT doesn't use an n-gram language model, so this will not change from None.
        self.config['ngram'] = None
        self.config['engine_name'] = 'hft'
        self.config['status'] = 'untrained'
        self.config['results'] = {}
        self.settings = {
            'word_delimiter_token': ' ',
            'num_train_epochs': 10,
            'min_duration_s': 0,
            'max_duration_s': 60,
            'learning_rate': 1e-4,
            'batch_size': 4,
            'debug': False,
            'data_split_train': 10,
            'data_split_val': 6,
        }
        print('model default settings', self.settings)

        self._setup_stages()

        # Use this when adding text to tensorboard so that we get to see predictions for each compute_metric run
        self.compute_metrics_count = 0

        # Use this to test audio - eg save resampled audio for listening to
        Path('/tmp/audio').mkdir(parents=True, exist_ok=True)
        self.tmp_audio_path = Path('/tmp/audio')

        # Prepare logging
        self.run_log_path = self.path.joinpath('train.log')
        self.config['run_log_path'] = self.run_log_path.as_posix()
        if not Path(self.run_log_path).is_file():
            run(f'touch {self.run_log_path};')
        sys.stdout = open(self.run_log_path, 'w')
        sys.stderr = sys.stdout

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dict = None
        return self

    @property
    def log(self):
        with open(self.config['run_log_path']) as logs:
            return logs.read()

    def _set_finished_training(self, has_finished: bool) -> None:
        self.status = FINISHED if has_finished else UNFINISHED

    def has_been_trained(self):
        return self.status == 'trained'

    def link(self, dataset: Dataset, _pron_dict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        # Note the _pron_dict is ignored as it's irrelevant to HFT.

    def build_structure(self):
        """
        HFT doesn't need file building like Kaldi does. However it does do a bunch of data processing.
        Could move that here, but for now let's leave it as is.
        """
        pass

    def get_arguments(self):
        """
        Build arguments from various sources (GUI, files, default, etc.).
        """
        keyword_arguments = {
            'elpis_data_dir': self.dataset.pathto.basepath.as_posix(),
            'train_size': '0.8',
            'split_seed': '42',
            'model_name_or_path': 'facebook/wav2vec2-large-xlsr-53',
            'output_dir': self.path.joinpath('wav2vec2'),
            'overwrite_output_dir': True,
            'num_train_epochs': int(self.settings['num_train_epochs']),
            'per_device_train_batch_size': int(self.settings['batch_size']),
            'per_device_eval_batch_size': int(self.settings['batch_size']),
            'gradient_accumulation_steps': '2',
            'learning_rate': self.settings['learning_rate'],
            'weight_decay': '0.005',
            'warmup_steps': '1000',
            'evaluation_strategy': 'steps',
            'save_steps': '500',
            'eval_steps': '500',
            'save_total_limit': '2',
            'gradient_checkpointing': True,
            'fp16': True if torch.cuda.is_available() else False,
            'group_by_length': True,
            'do_train': True,
            'do_eval': True,
            'logging_dir': self.path.joinpath('runs'),
        }

        if DEBUG:
            keyword_arguments.update(QUICK_TRAIN_BUILD_ARGUMENTS)

        arguments = [f'--{key}' if value is True else f'--{key}={value}'
            for key, value in keyword_arguments.items() if value]
        # See all possible arguments in src/transformers/training_args.py
        # or by passing the --help flag to this script.
        # We now keep distinct sets of args, for a cleaner separation of concerns.
        parser = HfArgumentParser((ModelArguments, DataTrainingArguments, TrainingArguments))
        if len(sys.argv) == 2 and sys.argv[1].endswith('.json'):
            # If we pass only one argument to the script and it's the path to a json file,
            # let's parse it to get our arguments.
            return parser.parse_json_file(json_file=Path(sys.argv[1]).resolve())
        else:
            return parser.parse_args_into_dataclasses(args=arguments)

    def get_last_checkpoint(self):
        """
        Detect last checkpoint.
        """
        last_checkpoint = None
        if Path(self.training_args.output_dir).is_dir() and self.training_args.do_train and not self.training_args.overwrite_output_dir:
            last_checkpoint = get_last_checkpoint(self.training_args.output_dir)
            if last_checkpoint is None and len(os.listdir(self.training_args.output_dir)) > 0:
                raise ValueError(
                    f'Output directory ({self.training_args.output_dir}) already exists and is not empty. '
                    'Use --overwrite_output_dir to overcome.')
            elif last_checkpoint is not None:
                logger.info(
                    f'Checkpoint detected, resuming training at {last_checkpoint}. To avoid this behavior, change '
                    'the `--output_dir` or add `--overwrite_output_dir` to train from scratch.')
        return last_checkpoint

    def _setup_stages(self):
        """
        Set up the stages used for displaying training information to the user.
        """
        self.index_prefixed_stages = [f'{i}_{stage}' for (i, stage) in enumerate(TRAINING_STAGES)]
        stage_labels = [string.capwords(stage).replace('_', ' ') for stage in TRAINING_STAGES]

        stage_names = {file: name for (file, name) in zip(self.index_prefixed_stages, stage_labels)}
        super().build_stage_status(stage_names)

    def _setup_logging(self) -> None:
        """
        Setup logging.
        """
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S',
            handlers=[logging.StreamHandler(sys.stdout)],)
        logger.setLevel(logging.INFO if is_main_process(self.training_args.local_rank) else logging.WARN)

        # Log on each process the small summary:
        logger.warning(
            f'Process rank: {self.training_args.local_rank}, '
            f'device: {self.training_args.device}, '
            f'n_gpu: {self.training_args.n_gpu}, '
            f'distributed training: {bool(self.training_args.local_rank != -1)}, '
            f'16-bits training: {self.training_args.fp16}'
        )
        # Set the verbosity to info of the Transformers logger (on main process only):
        # if is_main_process(training_args.local_rank):
        #     transformers.utils.logging.set_verbosity_info()
        logger.info(f'Training/evaluation parameters {self.training_args}')

    def get_language_data(self, data_dir, language_file='language_data.json'):
        """
        Use a json config file to prepare tokens.
        It is a simple json file with 2 flat lists (graphemes and removables).
        For now, this must be manually added to the /elpis dir.
        TODO add a GUI widget for this
        """
        language_data_path = Path('.').joinpath(language_file)
        if language_data_path.exists():
            with open(language_data_path) as fd:
                language_data = json.load(fd)
            logger.info(f'Language data: {language_data}')
        else:
            language_data = None
        return language_data

    def create_split(self, data_dir):
        """
        Create annotations files for the train/dev/test splits.
        """
        elpis_annotations_fn=(data_dir / 'annotations.json')
        with open(elpis_annotations_fn) as f:
            anno_json = json.load(f)

        train_annos, devtest_annos = train_test_split(
            anno_json,
            test_size=(1-self.data_args.train_size),
            random_state=self.data_args.split_seed
        )
        # Reduce the dataset size for debugging
        if DEBUG or self.settings['debug'] is True:
            train_annos = train_annos[:int(self.settings['data_split_train'])]
            devtest_annos = devtest_annos[:int(self.settings['data_split_val'])]

        # Make dev and test the same because we are mostly working with small datasets
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
            batch['text'] = batch['transcript']
            batch['path'] = str(data_dir / 'resampled' / batch['audio_file_name'])
            return batch
        ds = ds.map(make_text_col, remove_columns=['transcript', 'audio_file_name'])
        return ds

    def get_tokenizer(self, data_dir):
        file_name = self.create_vocabulary(data_dir, self.settings['word_delimiter_token'])

        tokenizer = Wav2Vec2CTCTokenizer(file_name,
                                         unk_token='[UNK]',
                                         pad_token='[PAD]',
                                         word_delimiter_token=self.settings['word_delimiter_token']
                                         )
        return tokenizer

    def create_vocabulary(self, data_dir, word_delimiter_token):
        language_data = self.get_language_data(data_dir)

        vocab_json_file = self.path.joinpath('vocab.json')

        def extract_all_chars(batch):
            all_text = ' '.join(batch['text'])
            vocab = list(set(all_text))
            return {'vocab': [vocab], 'all_text': [all_text]}

        vocab = self.hft_dataset['train'].map(
            extract_all_chars,
            batched=True,
            batch_size=-1,
            keep_in_memory=True,
            remove_columns=self.hft_dataset['train'].column_names,)
        vocab_list = list(set(vocab['vocab'][0]))
        naive_vocab_dict = {v: k for k, v in enumerate(vocab_list)}
        if language_data:
            if language_data.get('graphemes'):
                intelligent_vocab_dict = {}
                data_grapheme_duplications = set()
                for token in sorted(language_data['graphemes'], key=len):
                    if token not in intelligent_vocab_dict:
                        intelligent_vocab_dict[token] = len(intelligent_vocab_dict)
                    else:
                        data_grapheme_duplications.add(token)
                if data_grapheme_duplications:
                    logger.warning(f'{len(data_grapheme_duplications)} duplicated characters found and were ignored.\n'
                                   f'{" ".join(sorted(data_grapheme_duplications))}')
                naive_vocab_set = set(naive_vocab_dict)
                intelligent_vocab_set = set("".join(intelligent_vocab_dict))
                naive_specific_chars = naive_vocab_set - intelligent_vocab_set
                intelligent_specific_chars = intelligent_vocab_set - naive_vocab_set
                if naive_specific_chars:
                    for character in naive_specific_chars:
                        intelligent_vocab_dict[character] = len(intelligent_vocab_dict)
                        logger.warning(f'{len(naive_specific_chars)} characters found in data '
                                       f'but absent from language data and automatically added.\n'
                                       f'{" ".join(sorted(naive_specific_chars))}')
                if intelligent_specific_chars:
                    logger.warning(f'{len(intelligent_specific_chars)} characters found in language data '
                                   f'but absent in data.\n'
                                   f'{" ".join(sorted(intelligent_specific_chars))}')
                vocab_dict = intelligent_vocab_dict
        else:
            vocab_dict = naive_vocab_dict
        vocab_dict['[UNK]'] = len(vocab_dict)
        vocab_dict['[PAD]'] = len(vocab_dict)
        if word_delimiter_token in vocab_dict:
            logging.warning(f'The word delimiter token ({word_delimiter_token}) is present in the vocab dict.')
        if word_delimiter_token != ' ' and ' ' in vocab_dict:
            vocab_dict[word_delimiter_token] = vocab_dict.get(' ', len(vocab_dict))
            del vocab_dict[' ']
        with open(vocab_json_file, 'w') as vocab_file:
            json.dump(vocab_dict, vocab_file, ensure_ascii=False)
        return vocab_json_file

    def get_feature_extractor(self):
        return Wav2Vec2FeatureExtractor(
            feature_size=1, 
            sampling_rate=HFTModel.SAMPLING_RATE, 
            padding_value=0.0, 
            do_normalize=True, 
            return_attention_mask=True)

    def get_processor(self, feature_extractor, tokenizer):
        return Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)

    def get_model(self):
        return Wav2Vec2ForCTC.from_pretrained(
            self.model_args.model_name_or_path,
            cache_dir=self.model_args.cache_dir,
            activation_dropout=self.model_args.activation_dropout,
            attention_dropout=self.model_args.attention_dropout,
            hidden_dropout=self.model_args.hidden_dropout,
            feat_proj_dropout=self.model_args.feat_proj_dropout,
            mask_time_prob=self.model_args.mask_time_prob,
            gradient_checkpointing=self.model_args.gradient_checkpointing,
            layerdrop=self.model_args.layerdrop,
            ctc_loss_reduction='mean',
            pad_token_id=self.processor.tokenizer.pad_token_id,
            vocab_size=len(self.processor.tokenizer),
            ctc_zero_infinity=True)

    def preprocess_dataset(self):
        print('=== Preprocessing Dataset')
        speech = self.prepare_speech()

        def speech_file_to_array_fn(batch):
            path = batch['path']
            start_ms = batch['start_ms']
            stop_ms = batch['stop_ms']
            unique_key = f'{path}{start_ms}{stop_ms}'
            batch['speech'] = speech[unique_key]
            batch['sampling_rate'] = HFTModel.SAMPLING_RATE
            batch['target_text'] = batch['text']
            batch['duration'] = (batch['stop_ms'] - batch['start_ms'])/1000
            batch['duration'] = len(batch['speech'])/batch['sampling_rate']
            return batch

        self.hft_dataset = self.hft_dataset.map(
            speech_file_to_array_fn,
            remove_columns=self.hft_dataset['train'].column_names,
            num_proc=self.data_args.preprocessing_num_workers,
        )
        print('=== hft_dataset')
        print(self.hft_dataset)

    def prepare_dataset(self):
        print('=== Preparing Dataset')
        def prepare_dataset(batch):
            assert (
                len(set(batch['sampling_rate'])) == 1
            ), f'Make sure all inputs have the same sampling rate of {self.processor.feature_extractor.sampling_rate}.'
            batch['input_values'] = self.processor(batch['speech'], sampling_rate=batch['sampling_rate'][0]).input_values
            with self.processor.as_target_processor():
                batch['labels'] = self.processor(batch['target_text']).input_ids
            return batch

        self.hft_dataset = self.hft_dataset.map(
            prepare_dataset,
            remove_columns=self.hft_dataset['train'].column_names,
            batch_size=self.training_args.per_device_train_batch_size,
            batched=True,
            num_proc=self.data_args.preprocessing_num_workers,
        )

    def prepare_speech(self):
        print('=== Preparing Speech')
        speech = {}
        audio_paths = set()
        rejected_count = 0

        for utt in self.hft_dataset['train']:
            audio_paths.add((utt['path'], utt['text'], utt['start_ms'], utt['stop_ms']))

        for utt in self.hft_dataset['dev']:
            audio_paths.add((utt['path'], utt['text'], utt['start_ms'], utt['stop_ms']))

        for utt in self.hft_dataset['test']:
            audio_paths.add((utt['path'], utt['text'], utt['start_ms'], utt['stop_ms']))

        for path, text, start_ms, stop_ms in audio_paths:
            audio_metadata = torchaudio.info(path)

            start_frame = int(start_ms * (audio_metadata.sample_rate/1000))
            end_frame = int(stop_ms * (audio_metadata.sample_rate/1000))
            num_frames = end_frame - start_frame

            dur_ms = stop_ms - start_ms
            speech_array, sample_rate = torchaudio.load(filepath=path, frame_offset=start_frame, num_frames=num_frames)
            # Check that frames exceeds number of characters, wav file is not all zeros, and duration between min, max
            if (int(audio_metadata.num_frames) >= len(text) 
                    and speech_array.count_nonzero() 
                    and float(self.settings['min_duration_s']) < dur_ms/1000 < float(self.settings['max_duration_s'])):
                # Resample if required
                if sample_rate != HFTModel.SAMPLING_RATE:
                    print(f'Resample from {sample_rate} to {HFTModel.SAMPLING_RATE} | '
                          f'{os.path.basename(path).rjust(20)} | '
                          f'{str(start_ms/1000).rjust(15)} : {str(stop_ms/1000).ljust(15)} | '
                          f'{str(start_frame).rjust(15)} : {str(end_frame).ljust(15)}')
                    resampler = torchaudio.transforms.Resample(sample_rate, HFTModel.SAMPLING_RATE)
                    speech_array = resampler(speech_array)
                # Use a unique key for the speech key in case there are multiple annotations for audio files
                # i.e. don't use the audio file path as the key
                unique_key = f'{path}{start_ms}{stop_ms}'
                speech[unique_key] = speech_array.squeeze().numpy()
                # For debugging/ checking dataset, generate an audio file for listening
                # torchaudio.save(self.tmp_audio_path.joinpath(os.path.basename(path)), speech_array, HFTModel.SAMPLING_RATE)
            else:
                rejected_count += 1
                print(f'rejected {os.path.basename(path)} {start_ms} {stop_ms}')

        # Remove rejected speech by filtering on speech matching length the required conditions
        self.hft_dataset = self.hft_dataset.filter(lambda x: f'{path}{start_ms}{stop_ms}' in speech.keys())
        print(rejected_count, 'files removed due to number of frames, zero wav or too short')
        # Output some examples of the data for sanity check
        texts = [x['text'] for x in self.hft_dataset['train']]
        if len(texts) > 10:
            print(f'Random sample of {len(texts)} valid transcriptions from the original training set')
            print('\n'.join(random.choices(texts, k=10)))
        else:
            print(f'All {len(texts)} valid transcriptions from the original training set')
            print('\n'.join(texts))

        return speech

    def get_trainer(self, metric_name='wer'):
        # Metric
        metric = datasets.load_metric(metric_name)

        def compute_metrics(pred):
            self.compute_metrics_count = self.compute_metrics_count + 1
            pred_logits = pred.predictions
            pred_ids = np.argmax(pred_logits, axis=-1)
            pred.label_ids[pred.label_ids == -100] = self.processor.tokenizer.pad_token_id
            pred_str = self.processor.batch_decode(pred_ids)
            # we do not want to group tokens when computing the metrics
            label_str = self.processor.batch_decode(pred.label_ids, group_tokens=False)
            now = time.localtime()
            file_time_id = time.strftime('%Y%m%d_%H%M', now)
            all_predictions_str = ""
            # Build a string with all the reference text and prediction pairs
            for ref, pred in zip(label_str, pred_str):
                all_predictions_str = all_predictions_str + f'-----  \nR:  {ref}  \nP: {pred}  \n'
            # Write it to a text file
            with open(f'{self.training_args.output_dir}/dev_preds_{file_time_id}.txt', 'w') as f:
                f.write(all_predictions_str)
            # And add it to the tensorboard, with a timestamp so we retain these as training progresses
            self.tb_writer.add_text(f'Predictions {self.compute_metrics_count}', all_predictions_str)
            metric_result = metric.compute(predictions=pred_str, references=label_str)
            return {metric_name: metric_result}

        # Data collator
        data_collator = DataCollatorCTCWithPadding(processor=self.processor, padding=True)
        # Initialize our Trainer
        trainer = CTCTrainer(
            model=self.hft_model,
            data_collator=data_collator,
            args=self.training_args,
            compute_metrics=compute_metrics,
            train_dataset=self.hft_dataset['train'] if self.training_args.do_train else None,
            eval_dataset=self.hft_dataset['dev'] if self.training_args.do_eval else None,
            tokenizer=self.processor.feature_extractor,)
        trainer.tb_writer = self.tb_writer
        # Set a variable to track the total loss for a given epoch. (Unsure why
        # trainer doesn't do this; maybe in a later version of Transformers it
        # does.)
        trainer.epoch_loss = 0.0
        # Variable to track the last epoch we logged with tensorboard
        trainer.last_tb_epoch = 0
        return trainer

    def set_args(self, model_args, data_args, training_args):
        self.model_args = model_args
        self.data_args = data_args
        self.training_args = training_args
        print('\n\n=== Model args\n', model_args)
        print('\n\n=== Data args\n', data_args)
        print('\n\n=== Training args\n', training_args)

    def train(self, on_complete:Callable=None):
        self.tb_writer = SummaryWriter(self.path / 'runs')

        model_args, data_args, training_args = self.get_arguments()
        self.set_args(model_args, data_args, training_args)
        self._setup_logging()

        # Set seed before initializing model.
        set_seed(self.training_args.seed)

        # 1. Tokenization
        print('=== Tokenizing')
        self._set_finished_training(False)
        self._set_stage(TOKENIZATION)

        data_dir = Path(self.data_args.elpis_data_dir)
        self.create_split(data_dir)
        self.hft_dataset = self.get_dataset(data_dir)

        logging.info('Got dataset.')

        logging.info('Got dataset.')

        # Load pretrained model and tokenizer
        #
        # Distributed training:
        # The .from_pretrained methods guarantee that only one local process can concurrently download model & vocab.

        # TODO Get the device from the training args.
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f'Running on device: {device}.')

        tokenizer = self.get_tokenizer(data_dir)
        feature_extractor = self.get_feature_extractor()
        self.processor = self.get_processor(feature_extractor, tokenizer)
        self.hft_model = self.get_model()
        self.hft_model.to(device)

        self._set_stage(TOKENIZATION, complete=True)

        # 2. Preprocessing the datasets.
        # We need to read the audio files as arrays and tokenize the targets.
        self._set_stage(PREPROCESSING)
        self.preprocess_dataset()
        self.prepare_dataset()

        if self.model_args.freeze_feature_extractor:
            self.hft_model.freeze_feature_extractor()

        self._set_stage(PREPROCESSING, complete=True)

        print(f'len of dataset: {len(self.hft_dataset)}')

        # 3. Training
        self._set_stage(TRAIN)
        trainer = self.get_trainer()
        last_checkpoint = self.get_last_checkpoint()
        if self.training_args.do_train:
            # Update Checkpoint
            if last_checkpoint is not None:
                checkpoint = last_checkpoint
            elif Path(self.model_args.model_name_or_path).is_dir():
                checkpoint = self.model_args.model_name_or_path
            else:
                checkpoint = None
            # Train
            train_result = trainer.train(resume_from_checkpoint=checkpoint)
            # Log loss for final epoch in tensorboard.
            trainer.tb_writer.add_scalar('train/loss', trainer.epoch_loss, int(trainer.state.epoch)-1)
            trainer.save_model()

            # save the feature_extractor and the tokenizer
            if is_main_process(self.training_args.local_rank):
                self.processor.save_pretrained(self.training_args.output_dir)

            metrics = train_result.metrics
            metrics['train_samples'] = len(self.hft_dataset['train'])

            trainer.log_metrics(TRAIN, metrics)
            trainer.save_metrics(TRAIN, metrics)
            trainer.save_state()

        self._set_stage(TRAIN, complete=True)
        
        # 4. Evaluation
        self._set_stage(EVALUATION)
        if self.training_args.do_eval:
            logger.info('=== Evaluate')
            metrics = trainer.evaluate()
            metrics['eval_samples'] = len(self.hft_dataset['dev'])
            trainer.log_metrics('eval', metrics)
            trainer.save_metrics('eval', metrics)
            print('=== Metrics')
            print(metrics)
            self.config['results'] = metrics

        self._set_stage(EVALUATION, complete=True)
        self._set_finished_training(True)

    def _set_stage(self, stage: str, complete=False) -> None:
        """
        Updates the training stage to one of the constants specified within TRAINING_STAGES
        """
        if stage not in TRAINING_STAGES:
            return
        status = 'complete' if complete else 'in-progress'
        index = TRAINING_STAGES.index(stage)
        self.stage = self.index_prefixed_stages[index]
        self.stage_status = self.stage, status

    def get_train_results(self) -> Dict[str, float]:
        # comparison_val is a property common to all engines so the GUI can sort models by a result value
        results = {'comparison_val': float(self.config['results']['eval_wer']),
                   'wer': float(self.config['results']['eval_wer']),
                   'eval_loss': self.config['results']['eval_loss']
                   }
        return results
    

class ElpisTokenizer(Wav2Vec2CTCTokenizer):
    """
    Constructs an ElpisTokenizer tokenizer.

    This tokenizer inherits from :class:`~transformers.Wav2Vec2CTCTokenizer` which contains some of the main methods.
    Users should refer to the superclass for more information regarding such methods.
    The specificity of this specialized tokenizer is to manage complexe graphemes (when phonemes are coded on multiple
    characters) the same way as simple graphemes (see https://github.com/huggingface/transformers/issues/10942).
    It was then managed in a different way by an official PR on the main repository
    (https://github.com/huggingface/transformers/pull/11349) but I keep for the moment this method based on regular
    expressions because I prefer semantically not to manage complex graphemes in the same way as 'special tokens'.
    We should later test their method (and update our fork) to verify that everything works similarly.

    Args:
        vocab_file (:obj:`str`):
            File containing the vocabulary.
        bos_token (:obj:`str`, `optional`, defaults to :obj:`'<s>'`):
            The beginning of sentence token.
        eos_token (:obj:`str`, `optional`, defaults to :obj:`'</s>'`):
            The end of sentence token.
        unk_token (:obj:`str`, `optional`, defaults to :obj:`'<unk>'`):
            The unknown token. A token that is not in the vocabulary cannot be converted to an ID and is set to be this
            token instead.
        pad_token (:obj:`str`, `optional`, defaults to :obj:`'<pad>'`):
            The token used for padding, for example when batching sequences of different lengths.
        word_delimiter_token (:obj:`str`, `optional`, defaults to :obj:`'|'`):
            The token used for defining the end of a word.
        do_lower_case (:obj:`bool`, `optional`, defaults to :obj:`False`):
            Whether or not to accept lowercase input and lowercase the output when decoding.

        **kwargs
            Additional keyword arguments passed along to :class:`~transformers.PreTrainedTokenizer`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Characters which will disrupt the regex pattern business
        self.special_characters = ['?', '+', '*', '(', ')', '[', ']', '|']
        self.pattern: re.Pattern = self.get_pattern()

    def get_pattern(self) -> re.Pattern:
        exclusion_pattern = '|'.join([self.unk_token, self.bos_token, self.eos_token, self.pad_token])
        exclusion_pattern = re.sub(r'(\[|/)', r'\\\g<1>', exclusion_pattern)
        # logger.info(f'tokenizer – exclusion pattern: {exclusion_pattern}')
        graphemes = [key if key not in self.special_characters else f'\{key}' for key in self.encoder.keys() if
                     not re.match(exclusion_pattern, key, re.I)]
        logger.info(f'tokenizer – graphemes: {graphemes}')
        pattern = re.compile('|'.join(sorted(graphemes, key=lambda grapheme: len(grapheme), reverse=True)))
        logger.info(f'tokenizer – tokenization pattern: {pattern}')
        return pattern

    def _tokenize(self, text: str) -> List[str]:
        """
        Converts a string in a sequence of tokens (string), using the tokenizer.
        """
        if self.do_lower_case:
            text = text.upper()
        tokens = re.findall(self.pattern, text)
        return tokens


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune from.
    """

    model_name_or_path: str = field(
        metadata={
            'help': 'Path to pretrained model or model identifier from huggingface.co/models.'
        }
    )
    cache_dir: Optional[str] = field(
        default=None,
        metadata={
            'help': 'Where you want to store the pretrained models downloaded from huggingface.co.'
        },
    )
    freeze_feature_extractor: Optional[bool] = field(
        default=True,
        metadata={
            'help': 'Whether to freeze the feature extractor layers of the model.'
        },
    )
    attention_dropout: Optional[float] = field(
        default=0.1,
        metadata={'help': 'The dropout ratio for the attention probabilities.'},
    )
    activation_dropout: Optional[float] = field(
        default=0.1,
        metadata={
            'help': 'The dropout ratio for activations inside the fully connected layer.'
        },
    )
    hidden_dropout: Optional[float] = field(
        default=0.1,
        metadata={
            'help': 'The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.'
        },
    )
    feat_proj_dropout: Optional[float] = field(
        default=0.0,
        metadata={
            'help': 'The dropout probability for all 1D convolutional layers in feature extractor.'
        },
    )
    mask_time_prob: Optional[float] = field(
        default=0.05,
        metadata={
            'help': 'Probability of each feature vector along the time axis to be chosen as the start of the vector'
            'span to be masked. Approximately ``mask_time_prob * sequence_length // mask_time_length`` feature'
            'vectors will be masked along the time axis. This is only relevant if ``apply_spec_augment is True``.'
        },
    )
    gradient_checkpointing: Optional[bool] = field(
        default=True,
        metadata={
            'help': 'If True, use gradient checkpointing to save memory at the expense of slower backward pass.'
        },
    )
    layerdrop: Optional[float] = field(
        default=0.0, metadata={'help': 'The LayerDrop probability.'}
    )

@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    elpis_data_dir: str = field(
        metadata={
            'help': 'The path to the directory containing Elpis-preprocessed data.'
        }
    )
    train_size: Optional[float] = field(
        default=0.8,
        metadata={
            'help': 'The fraction of the data used for training. The rest is split evenly between the dev and test sets.'
        },
    )
    split_seed: Optional[int] = field(
        default=42,
        metadata={'help': 'The random seed used to create the train/dev/test splits.'},
    )
    dataset_config_name: Optional[str] = field(
        default=None,
        metadata={
            'help': 'The configuration name of the dataset to use (via the datasets library).'
        },
    )
    train_split_name: Optional[str] = field(
        default='train+validation',
        metadata={
            'help': 'The name of the training data set split to use (via the datasets library). Defaults to "train"'
        },
    )
    overwrite_cache: bool = field(
        default=False,
        metadata={'help': 'Overwrite the cached preprocessed datasets or not.'},
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={'help': 'The number of processes to use for the preprocessing.'},
    )
    chars_to_ignore: List[str] = list_field(
        default=[',', '?', '.', '!', '-', ';', ':', '""', '%', ''', ''', '�'],
        metadata={'help': 'A list of characters to remove from the transcripts.'},
    )

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
        input_features = [{'input_values': feature['input_values']} for feature in features]
        label_features = [{'input_ids': feature['labels']} for feature in features]
        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            max_length=self.max_length,
            pad_to_multiple_of=self.pad_to_multiple_of,
            return_tensors='pt',
        )
        with self.processor.as_target_processor():
            labels_batch = self.processor.pad(
                label_features,
                padding=self.padding,
                max_length=self.max_length_labels,
                pad_to_multiple_of=self.pad_to_multiple_of_labels,
                return_tensors='pt',
            )
        # replace padding with -100 to ignore loss correctly
        labels = labels_batch['input_ids'].masked_fill(labels_batch.attention_mask.ne(1), -100)
        batch['labels'] = labels
        return batch


class CTCTrainer(Trainer):
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
        # When we've finished the previous epoch, log the loss for that epoch in tensorboard.
        if int(self.state.epoch) > self.last_tb_epoch:
            self.tb_writer.add_scalar('train/loss', self.epoch_loss, int(self.state.epoch)-1)
            self.last_tb_epoch = int(self.state.epoch)
            self.epoch_loss = 0.0

        model.train()
        inputs = self._prepare_inputs(inputs)

        if self.use_amp:
            with autocast():
                loss = self.compute_loss(model, inputs)
        else:
            loss = self.compute_loss(model, inputs)

        if self.args.n_gpu > 1:
            if model.module.config.ctc_loss_reduction == 'mean':
                loss = loss.mean()
            elif model.module.config.ctc_loss_reduction == 'sum':
                loss = loss.sum() / (inputs['labels'] >= 0).sum()
            else:
                raise ValueError(f'{model.config.ctc_loss_reduction} is not valid. Choose one of ["mean", "sum"]')

        if self.args.gradient_accumulation_steps > 1:
            loss = loss / self.args.gradient_accumulation_steps

        if self.use_amp:
            self.scaler.scale(loss).backward()
        elif self.use_apex:
            with amp.scale_loss(loss, self.optimizer) as scaled_loss:
                scaled_loss.backward()
        elif self.deepspeed:
            self.deepspeed.backward(loss)
        else:
            loss.backward()

        self.epoch_loss += loss.item()
        return loss.detach()


# For dev test purpose (to run without the GUI)…
if __name__ == '__main__':
    model = HFTModel(parent_path='..')
    model.train()
