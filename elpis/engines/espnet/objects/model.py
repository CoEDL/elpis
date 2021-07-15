""" Support for training ESPnet models."""
import os
from pathlib import Path
import re
import shutil
import subprocess
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
        self.config['engine_name'] = 'espnet'
        self.config['status'] = 'untrained'
        stage_names = {
            "train": "Train"
        }
        super().build_stage_status(stage_names)
        self.venv_path = Path("/espnet/tools/venv/bin/python3")
        self.config['gpus'] = int(subprocess.check_output(f"{self.venv_path} -c 'import torch; print(torch.cuda.device_count())'", shell=True))
        print(f"Number of GPUs: {self.config['gpus']}")

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dict = None
        return self

    @property
    def status(self):
        #  read the log here and pass it back to the api
        run_log_path = Path(self.path).joinpath('train.log')
        if not Path(run_log_path).is_file():
            run(f"touch {run_log_path};")
        with open(run_log_path) as log_file:
            log_text = log_file.read()
            self.stage_status = ("train", 'in-progress', '', log_text)
        # Stage 4 train log is not written to the main train log, so read it from the exp dir
        is_stage_4 = re.search('stage 4: Network Training\n\Z', log_text, flags=re.MULTILINE)

        if is_stage_4:
            #  Train stage 4 log is in the exp dir... something like exp/train_nodev_pytorch_train_mtlalpha1.0
            path_gen = Path(self.path).glob("espnet-asr1/exp/train*/train.log")
            # Assumes just one decode_test* directory, which is true in the current
            # implementation (transcription will use decode_infer*...)
            stage_4_log_path= next(path_gen)
            with open(stage_4_log_path) as stage_4_log_file:
                stage_4_text = stage_4_log_file.read()
                self.stage_status = ("train", "in-progress", "", f"{log_text}\n{stage_4_text}")
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def has_been_trained(self):
        return self.status == 'trained'

    def link(self, dataset: Dataset, _pron_dict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        # Note the _pron_dict is ignored as it's irrelevant to ESPnet.

    def build_structure(self):
        print("BUILD STRUCTURE")
        # NOTE Since the ESPnet data is similar to Kaldi in terms of formatting requirements,
        # code is unfortunately being duplicated from KaldiModel.
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
            local_espnet_path = model_path.joinpath("espnet-asr1")
            shutil.copytree("/espnet/egs/elpis/asr1", f"{local_espnet_path}")

            # Then move the train/test data across.
            src_train_dir = model_path.joinpath("output/training")
            tgt_train_dir = local_espnet_path.joinpath("data/train")
            shutil.copytree(src_train_dir, tgt_train_dir)

            src_test_dir = model_path.joinpath("output/testing")
            tgt_test_dir = local_espnet_path.joinpath("data/test")
            shutil.copytree(src_test_dir, tgt_test_dir)

            # Then move the WAVs across
            src_wav_dir = Path(self.dataset.path).joinpath("resampled")
            for wav in src_wav_dir.glob("*.wav"):
                shutil.copy(wav, local_espnet_path)

        def train():
            local_espnet_path = Path(self.path).joinpath("espnet-asr1")
            run_log_path = Path(self.path).joinpath('train.log')
            print(f"SELF PATH {self.path}")
            if os.path.isfile(run_log_path):
                os.remove(run_log_path)
            try:
                p = run(f"cd {local_espnet_path}; ./run.sh --ngpu {self.config['gpus']} --nj 1 &> {run_log_path}")
                print('done')
                self.status = 'trained'
            except subprocess.CalledProcessError as e:
                with open(run_log_path, 'a+') as file:
                    print('stderr', e.stderr, file=file)
                    print('failed', file=file)
                print('failed')
                self.status = f'failed with code {e.returncode}'

        def run_training_in_background():
            def background_train_task():
                prepare_for_training()
                train()                
                self.results = EspnetModel.get_train_results(self)
                on_complete()
            self.status = 'training'
            t = threading.Thread(target=background_train_task)
            t.start()

        if on_complete is None:
            print("oncomplete is none")
            self.status = 'training'
            prepare_for_training()
            train()
            self.status = 'trained'
            self.results = EspnetModel.get_train_results(self)
        else:
            print("oncomplete is not none")
            run_training_in_background()
        return

    def get_train_results(self):
        path_gen = Path(self.path).glob("espnet-asr1/exp/train*/decode_test*/result.txt")
        # Assumes just one decode_test* directory, which is true in the current
        # implementation (transcription will use decode_infer*...)
        log_file = next(path_gen)
        with open(log_file) as f:
            text = f.read()

        # Regex to detect floating point numbers
        val = r"[^ ]+"
        avg_line_re = (rf"Sum/Avg *\| *\d+ *\d+ *\| *{val} *" +
                       rf"(?P<sub>{val}) *(?P<del>{val}) *(?P<ins>{val}) *(?P<per>{val}) *{val}"
                       )
        try:
            sub = re.search(avg_line_re, text).group("sub")
            del_ = re.search(avg_line_re, text).group("del")
            ins = re.search(avg_line_re, text).group("ins")
            per = re.search(avg_line_re, text).group("per")
        except AttributeError:
            per = sub = ins = del_ = None

        results = {"comparison_val": float(per),  # property common to all engines so the GUI can sort models by a result value
                   "per": float(per),
                   "ins_val": int(float(ins)),
                   "del_val": int(float(del_)),
                   "sub_val": int(float(sub))}

        print(results)
        return results
