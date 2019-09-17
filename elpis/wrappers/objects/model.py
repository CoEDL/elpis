import pystache
import os
import shutil
from io import BufferedIOBase
from pathlib import Path
from typing import Callable
import threading
from elpis.wrappers.objects.command import run
from elpis.wrappers.objects.dataset import Dataset
from elpis.wrappers.objects.pron_dict import PronDict
from elpis.wrappers.objects.fsobject import FSObject
from elpis.wrappers.input.json_to_kaldi import create_kaldi_structure
from elpis.wrappers.objects.path_structure import KaldiPathStructure



class ModelFiles(object):
    def __init__(self, basepath: Path):
        self.kaldi = KaldiPathStructure(basepath)


# TODO not thread safe
class Model(FSObject):
    _config_file = 'model.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset: Dataset = None
        self.config['dataset_name'] = None  # dataset hash has not been linked
        self.pron_dict: PronDict = None
        self.config['pron_dict_name'] = None  # pron_dict hash has not been linked
        self.config['ngram'] = 1 # default to 1 to make playing quicker
        self.config['status'] = 'untrained'
        self.status = 'untrained'

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.dataset = None
        self.pron_dict = None
        return self

    @property
    def status(self):
        return self.config['status']

    @status.setter
    def status(self, value: str):
        self.config['status'] = value

    def link(self, dataset: Dataset, pron_dict: PronDict):
        self.dataset = dataset
        self.config['dataset_name'] = dataset.name
        self.pron_dict = pron_dict
        self.config['pron_dict_name'] = pron_dict.name

    @property
    def ngram(self) -> int:
        return int(self.config['ngram'])

    @ngram.setter
    def ngram(self, value: int) -> None:
        self.config['ngram'] = value


    def build_kaldi_structure(self):
        # task json-to-kaldi
        output_path = self.path.joinpath('output')
        output_path.mkdir(parents=True, exist_ok=True)
        text_corpus_path = self.path.joinpath('text_corpus')
        text_corpus_path.mkdir(parents=True, exist_ok=True)
        corpus_file_path = self.path.joinpath('corpus.txt')
        create_kaldi_structure(
            input_json=f'{self.dataset.pathto.filtered_json}',
            output_folder=f'{output_path}',
            silence_markers=None,
            text_corpus=f'{text_corpus_path}',
            corpus_file=f'{corpus_file_path}'
        )

    def train(self, on_complete:Callable=None):

        def prepare_for_training():
            # task make-kaldi-subfolders
            kaldi_structure = KaldiPathStructure(self.path)

            local_kaldi_path = self.path.joinpath('kaldi')
            local_kaldi_path.mkdir(parents=True, exist_ok=True)
            kaldi_data_local_dict = local_kaldi_path.joinpath('data', 'local', 'dict')
            kaldi_data_local_dict.mkdir(parents=True, exist_ok=True)
            kaldi_data_local = local_kaldi_path.joinpath('data', 'local')
            kaldi_data_local.mkdir(parents=True, exist_ok=True)
            kaldi_data_test = local_kaldi_path.joinpath('data', 'test')
            kaldi_data_test.mkdir(parents=True, exist_ok=True)
            kaldi_data_train = local_kaldi_path.joinpath('data', 'train')
            kaldi_data_train.mkdir(parents=True, exist_ok=True)
            kaldi_conf = local_kaldi_path.joinpath('conf')
            kaldi_conf.mkdir(parents=True, exist_ok=True)
            kaldi_local = local_kaldi_path.joinpath('local')
            kaldi_local.mkdir(parents=True, exist_ok=True)

            # copy the pron dict
            shutil.copy(f"{self.pron_dict.lexicon_txt}", f"{kaldi_data_local_dict.joinpath('lexicon.txt')}")

            # task generate-kaldi-configs
            path_file_path = kaldi_structure.path.joinpath('path.sh')
            mfcc_file_path = kaldi_structure.conf.joinpath('mfcc.conf')
            decode_config_file_path = kaldi_structure.conf.joinpath('decode.config')

            template_path = Path('/elpis/elpis/wrappers/templates')
            path_resource = template_path.joinpath('path.sh')
            mfcc_resource = template_path.joinpath('mfcc.conf')
            decode_config_resource = template_path.joinpath('decode.config')

            # task make-nonsil-phones > {{ .KALDI_OUTPUT_PATH }}/tmp/nonsilence_phones.txt
            nonsilence_phones_path = kaldi_data_local_dict.joinpath('nonsilence_phones.txt')
            cmd = f"grep -v '^#' < {self.pron_dict.l2s_path} | cut -d' ' -f2 | grep -v '^$' | sort -u | uniq -c"
            p = run(cmd)
            with nonsilence_phones_path.open(mode='wb') as fout:
                fout.write(p.stdout)

            with path_file_path.open(mode='w') as fout:
                with path_resource.open() as fin:
                    content = pystache.render(
                        fin.read(),
                        {
                            'KALDI_ROOT': '/kaldi',
                            'HELPERS_PATH': '/kaldi-helpers',
                            'CORPUS_PATH': f'..{self.dataset.pathto.original}'
                        }
                    )
                    fout.write(content)

            with mfcc_file_path.open(mode='w') as fout:
                with mfcc_resource.open() as fin:
                    content = pystache.render(
                        fin.read(),
                        {
                            'MFCC_SAMPLE_FREQUENCY': '44100',
                            'MFCC_FRAME_LENGTH': '25',
                            'MFCC_LOW_FREQ': '20',
                            'MFCC_HIGH_FREQ': '22050',
                            'MFCC_NUM_CEPS': '7',
                        }
                    )
                    fout.write(content)

            with decode_config_file_path.open(mode='w') as fout:
                with decode_config_resource.open() as fin:
                    content = pystache.render(
                        fin.read(),
                        {
                            'DECODE_BEAM': '11.0',
                            'DECODE_FIRST_BEAM': '8.0'
                        }
                    )
                    fout.write(content)
            try:
                # task copy-generated-files
                output_path = self.path.joinpath('output')
                output_path.mkdir(parents=True, exist_ok=True)

                # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/corpus.txt {{ .KALDI_OUTPUT_PATH }}/kaldi/data/local/
                shutil.move(f"{output_path.joinpath('training', 'corpus.txt')}", f"{kaldi_data_local}")

                # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/segments {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/
                # testing/text {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/utt2spk {{ .KALDI_OUTPUT_PATH }}/tmp/json_
                # splitted/testing/wav.scp {{ .KALDI_OUTPUT_PATH }}/kaldi/data/test/
                shutil.move(f"{output_path.joinpath('testing', 'segments')}", f"{kaldi_data_test.joinpath('segments')}")
                shutil.move(f"{output_path.joinpath('testing', 'text')}", f"{kaldi_data_test.joinpath('text')}")
                shutil.move(f"{output_path.joinpath('testing', 'utt2spk')}", f"{kaldi_data_test.joinpath('utt2spk')}")
                shutil.move(f"{output_path.joinpath('testing', 'wav.scp')}", f"{kaldi_data_test.joinpath('wav.scp')}")
                # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/segments {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted
                # /training/text {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/utt2spk {{ .KALDI_OUTPUT_PATH }}/tmp/json
                # _splitted/training/wav.scp {{ .KALDI_OUTPUT_PATH }}/kaldi/data/train/
                shutil.move(f"{output_path.joinpath('training', 'segments')}", f"{kaldi_data_train.joinpath('segments')}")
                shutil.move(f"{output_path.joinpath('training', 'text')}", f"{kaldi_data_train.joinpath('text')}")
                shutil.move(f"{output_path.joinpath('training', 'utt2spk')}", f"{kaldi_data_train.joinpath('utt2spk')}")
                shutil.move(f"{output_path.joinpath('training', 'wav.scp')}", f"{kaldi_data_train.joinpath('wav.scp')}")

                # task copy-phones-configs
                optional_silence_file_path = kaldi_data_local_dict.joinpath('optional_silence.txt')
                silence_phones_file_path = kaldi_data_local_dict.joinpath('silence_phones.txt')
                with optional_silence_file_path.open(mode='w') as fout:
                    fout.write('SIL\n')
                with silence_phones_file_path.open(mode='w') as fout:
                    fout.write('SIL\nsil\nspn\n')

                # task copy-helper-scripts
                # - cp {{ .KALDI_TEMPLATES }}/cmd.sh {{ .KALDI_OUTPUT_PATH }}/kaldi/
                shutil.copy(f"{template_path.joinpath('cmd.sh')}", f"{local_kaldi_path}")
                # - cp {{ .KALDI_TEMPLATES }}/run.sh {{ .KALDI_OUTPUT_PATH }}/kaldi/
                with open(f"{template_path.joinpath('run.sh')}", 'r') as fin, \
                        open(f"{local_kaldi_path.joinpath('run.sh')}", 'w') as fout:
                    fout.write(fin.read().replace('lm_order=1', f"lm_order={self.ngram}"))
                os.chmod(f"{local_kaldi_path.joinpath('run.sh')}", 0o774)
                # - cp {{ .KALDI_TEMPLATES }}/score.sh {{ .KALDI_OUTPUT_PATH }}/kaldi/local/
                shutil.copy(f"{template_path.joinpath('score.sh')}", f"{kaldi_local}")
                # - cp -L -r {{ .KALDI_ROOT }}/egs/wsj/s5/steps {{ .KALDI_OUTPUT_PATH }}/kaldi/steps
                run(f"cp -L -r /kaldi/egs/wsj/s5/steps {local_kaldi_path}/steps")
                # - cp -L -r {{ .KALDI_ROOT }}/egs/wsj/s5/utils {{ .KALDI_OUTPUT_PATH }}/kaldi/utils
                run(f"cp -L -r /kaldi/egs/wsj/s5/utils {local_kaldi_path}/utils")

                # modified extract-wavs
                for audio_file in os.listdir(self.dataset.pathto.resampled):
                    src = f'{self.dataset.pathto.resampled.joinpath(audio_file)}'
                    dst = f'{local_kaldi_path}'
                    shutil.copy(src, dst)
                print('kaldi dirs preparation done.')
            except BaseException as e:
                print('couldnt prepare kaldi dirs: ', e)

        def train():
            local_kaldi_path = self.path.joinpath('kaldi')

            # Setup for Training complete
            ######################################################################

            # task _test-train
            tmp_log_path = '/elpis/state/tmp_log.txt'
            if os.path.isfile(tmp_log_path):
                os.remove(tmp_log_path)
            p = run(f"cd {local_kaldi_path}; ./run.sh > {tmp_log_path}")
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
            self.status = 'training'
            prepare_for_training()
            train()
            self.status = 'trained'
        else:
            run_training_in_background()
        return
