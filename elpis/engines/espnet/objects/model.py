""" Support for training ESPnet models."""
import os
from pathlib import Path
import shutil
import threading
from typing import Callable

from elpis.engines.common.objects.command import run
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.model import Model as BaseModel
from elpis.engines.kaldi.input.json_to_kaldi import create_kaldi_structure


class EspnetModel(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ESPnet does not use a pronunciation dictionary so this will not
        # change from None.
        self.pron_dict = None
        self.config['pron_dict_name'] = None
        # ESPnet doesn't use an n-gram language model, so this will not change
        # from None.
        self.config['ngram'] = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dict = None
        return self

    @property
    def status(self):
        return self.config['status']

    @property
    def state(self):
        # In the KaldiModel that I'm basing this code of there is a "TODO: fix
        # this" in this method. I'm not sure what that's about.
        return {}

    def has_been_trained(self):
        return self.status == 'trained'

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def link(self, dataset: Dataset, _pron_dict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        # Note the _pron_dict is ignored as it's irrelevant to ESPnet.

    def build_structure(self):
        print("BUILD STRUCTURE")
        # NOTE Since the ESPnet data is similari informatting requirements to
        # Kaldi structure, code is unfortunately being duplicated from KaldiModel.
        # I'm not sure the best way to get around this, but calling create_kaldi_structure()
        # here does limit that duplication somewhat.
        output_path = self.path.joinpath('output')
        output_path.mkdir(parents=True, exist_ok=True)

        print("OUTPUT PATH: {}".format(output_path))

        # Copy cleaned corpus from dataset to the model
        dataset_corpus_txt = self.dataset.path.joinpath('cleaned', 'corpus.txt')
        model_corpus_txt = self.path.joinpath('corpus.txt')
        if os.path.exists(dataset_corpus_txt):
            shutil.copy(f'{dataset_corpus_txt}', f'{model_corpus_txt}')
        create_kaldi_structure(
            input_json=f'{self.dataset.pathto.annotation_json}',
            output_folder=f'{output_path}',
            silence_markers=False,
            corpus_txt=f'{model_corpus_txt}'
        )

    def train(self, on_complete:Callable=None):

        def prepare_for_training():
            # This should just copy the ESPnet experiment directory into the
            # model directory and then copy the prepared train/test langdir
            # stuff into the appropriate subdirectory.

            # First make a copy of the ESPNET Elpis recipe
            model_path = Path(self.path)
            local_espnet_path = model_path / "espnet-asr1"
            shutil.copytree("/espnet/egs/elpis/asr1", f"{local_espnet_path}")

            # Then move the train/test data across.
            src_train_dir = model_path / "output" / "training"
            tgt_train_dir = local_espnet_path / "data" / "train"
            shutil.copytree(src_train_dir, tgt_train_dir)

            src_test_dir = model_path / "output" / "testing"
            tgt_test_dir = local_espnet_path / "data" / "test"
            shutil.copytree(src_test_dir, tgt_test_dir)

            # Then move the WAVs across
            src_wav_dir = Path(self.dataset.path) / "resampled"
            for wav in src_wav_dir.glob("*.wav"):
                shutil.copy(wav, local_espnet_path)
            #shutil.copytree(src_wav_dir, local_espnet_path, dirs_exist_ok=True)

        def train():
            local_espnet_path = Path(self.path) / 'espnet-asr1'
            run_log_path = Path(self.path) / 'train.log'
            print("SELF PATH {}".format(self.path))
            if os.path.isfile(run_log_path):
                os.remove(run_log_path)
            p = run(f"cd {local_espnet_path}; ./run.sh --nj 1 &> {run_log_path}")
            print(p.stdout)
            print('train double done.')

        def run_training_in_background():
            def background_train_task():
                prepare_for_training()
                train()
                self.status = 'trained'
                on_complete()
            self.status = 'training'
            t = threading.Thread(target=background_train_task)
            t.start()

        if on_complete is None:
            print("oncomplete is none")
        else:
            print("oncomplete is not none")
            run_training_in_background()
        return

    def get_train_results(self):
        from pathlib import Path
        path_gen = Path(self.path).glob("espnet-asr1/exp/train*/decode*/result.txt")
        log_file = next(path_gen) # TODO Assumes just one decode directory, but if we apply the same model to data several times, this won't be true.

        with open(log_file) as f:
            sum_avg_line = f.readlines()[34]
            per = sum_avg_line.split()[-3]
            ins = sum_avg_line.split()[-4]
            del_ = sum_avg_line.split()[-5]
            sub = sum_avg_line.split()[-6]
        results = {"per": per,
                   "sub_val": sub,
                   "ins_val": ins,
                   "del_val": del_}
        print(results)
        return results