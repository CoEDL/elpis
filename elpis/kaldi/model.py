import pystache
import os
import shutil
from io import BufferedIOBase
from pathlib import Path
from typing import Callable
from .command import run
from .dataset import Dataset
from .fsobject import FSObject
from .path_structure import KaldiPathStructure
from kaldi_helpers.input_scripts.json_to_kaldi import create_kaldi_structure
from kaldi_helpers.input_scripts.make_wordlist import generate_word_list
from kaldi_helpers.input_scripts.make_prn_dict import generate_pronunciation_dictionary


class ModelFiles(object):
    def __init__(self, basepath: Path):
        self.kaldi = KaldiPathStructure(basepath)


class Model(FSObject):
    _config_file = 'model.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.l2s_path = self.path.joinpath('l2s.txt')
        self.lexicon_txt = self.path.joinpath('kaldi', 'data', 'local', 'dict', 'lexicon.txt')
        self.dataset: Dataset
        self.config['dataset'] = None  # dataset hash has not been linked
        self.config['l2s'] = None  # file has not been uploaded
        self.config['ngram'] = 3
        self.dataset = None

    def set_l2s_path(self, path: Path):
        path = Path(path)
        with path.open(mode='rb') as fin:
            self.set_l2s_fp(fin)

    def set_l2s_fp(self, file: BufferedIOBase):
        self.set_l2s_content(file.read())

    def set_l2s_content(self, content: str):
        # TODO: this function uses parameter str, and must be bytes or UTF-16
        self.config['l2s'] = True
        with self.l2s_path.open(mode='wb') as fout:
            fout.write(content)

    @property
    def l2s(self):
        with self.l2s_path.open(mode='rb') as fin:
            return fin.read()

    def link(self, dataset: Dataset):
        self.dataset = dataset
        self.config['dataset'] = dataset.hash

    @property
    def ngram(self) -> int:
        return int(self.config['ngram'])

    @ngram.setter
    def ngram(self, value: int) -> None:
        self.config['ngram'] = value

    def generate_lexicon(self):
        # task make-kaldi-subfolders
        temporary_path = Path('/tmp', self.hash)
        temporary_path.mkdir(parents=True, exist_ok=True)

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

        # task make-prn-dict
        # TODO this file needs to be reflected in kaldi_data_local_dict
        generate_pronunciation_dictionary(word_list=f'{self.dataset.pathto.word_list_txt}',
                                          pronunciation_dictionary=f'{self.lexicon_txt}',
                                          config_file=f'{self.l2s_path}')
    @property
    def lexicon(self):
        with self.lexicon_txt.open(mode='rb') as fin:
            return fin.read()

    def train(self, on_complete:Callable=None):
        def prepare_for_training():
            # task make-kaldi-subfolders
            kaldi_structure = KaldiPathStructure(self.path)
            temporary_path = Path('/tmp', self.hash)
            temporary_path.mkdir(parents=True, exist_ok=True)

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

            # task generate-kaldi-configs
            path_file_path = kaldi_structure.path.joinpath('path.sh')
            mfcc_file_path = kaldi_structure.conf.joinpath('mfcc.conf')
            decode_config_file_path = kaldi_structure.conf.joinpath('decode.config')

            template_path = Path('/kaldi-helpers/resources/kaldi_templates')
            path_resource = template_path.joinpath('path.sh')
            mfcc_resource = template_path.joinpath('mfcc.conf')
            decode_config_resource = template_path.joinpath('decode.config')

            # task make-nonsil-phones > {{ .KALDI_OUTPUT_PATH }}/tmp/nonsilence_phones.txt
            nonsilence_phones_path = kaldi_data_local_dict.joinpath('nonsilence_phones.txt')
            cmd = f"grep -v '^#' < {self.pronunciation_path} | cut -d' ' -f2 | grep -v '^$' | sort -u"
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

            # task copy-generated-files
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
            print('done.')
        def train():
            local_kaldi_path = self.path.joinpath('kaldi')

            # Setup for Training complete
            ######################################################################

            # task _test-train
            p = run(f"cd {local_kaldi_path}; ./run.sh")
            print(p.stdout)
            print('double done.')
        prepare_for_training()
        train()
        return
