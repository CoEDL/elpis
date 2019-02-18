from . import hasher
from .session import Session
from .command import run
from .dataset import Dataset
from pathlib import Path
import pystache
import os
import shutil
from io import BufferedIOBase
from kaldi_helpers.input_scripts import create_kaldi_structure, generate_word_list, generate_pronunciation_dictionary


class Model(object):
    def __init__(self, basepath: Path, name:str, sesson: Session):
        super().__init__()
        self.name: str = name
        self.hash: str = hasher.new()
        self.path: Path = basepath.joinpath(self.hash)
        self.path.mkdir(parents=True, exist_ok=True)
        self.pronunciation_path = self.path.joinpath('pron.txt')
        self.dataset: Dataset

    def set_pronunciation_content(self, content: str):
        with self.pronunciation_path.open(mode='wb') as fout:
            fout.write(content)

    def set_pronunciation_path(self, path: Path):
        path = Path(path)
        with path.open(mode='rb') as fin:
            self.set_pronunciation_fp(fin)
        
    def set_pronunciation_fp(self, file: BufferedIOBase):
        self.set_pronunciation_content(file.read())

    def link(self, dataset: Dataset):
        self.dataset = dataset

    def train(self):
        # task make-kaldi-subfolders
        local_kaldi_path = self.path.joinpath('kaldi')
        local_kaldi_path.mkdir(parents=True, exist_ok=True)
        kaldi_data_local_dict = local_kaldi_path.joinpath( 'data', 'local', 'dict')
        kaldi_data_local_dict.mkdir(parents=True, exist_ok=True)
        kaldi_data_local = local_kaldi_path.joinpath( 'data', 'local')
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
        path_file_path = local_kaldi_path.joinpath('path.sh')
        mfcc_file_path = kaldi_conf.joinpath('mfcc.conf')
        decode_config_file_path = kaldi_conf.joinpath('decode.config')

        template_path = Path('/kaldi-helpers/resources/kaldi_templates')
        path_resource = template_path.joinpath('path.sh')
        mfcc_resource = template_path.joinpath('mfcc.conf')
        decode_config_resource = template_path.joinpath('decode.config')

        
        # task json-to-kaldi
        output_path = self.path.joinpath('output')
        output_path.mkdir(parents=True, exist_ok=True)
        text_corpus_path = self.path.joinpath('text_corpus')
        text_corpus_path.mkdir(parents=True, exist_ok=True)
        corpus_file_path = self.path.joinpath('corpus.txt')
        create_kaldi_structure(
            input_json=f'{self.dataset.elan_json_path}',
            output_folder=f'{output_path}',
            silence_markers=None,
            text_corpus=f'{text_corpus_path}',
            corpus_file=f'{corpus_file_path}'
        )

        # task make-wordlist
        word_list_path = self.path.joinpath('wordlist.txt')
        additional_words_path = self.path.joinpath('additional_words_path.txt') # TODO: does not exist
        generate_word_list(transcription_file=f'{self.dataset.elan_json_path}',
                       word_list_file=f'{additional_words_path}',
                       output_file=f'{word_list_path}',
                       kaldi_corpus_file=f'{corpus_file_path}')


        # task make-prn-dict
        lexicon_file_path = kaldi_data_local_dict.joinpath('lexicon.txt')
        generate_pronunciation_dictionary(word_list=f'{word_list_path}',
                                      pronunciation_dictionary=f'{lexicon_file_path}',
                                      config_file=f'{self.pronunciation_path}')
        

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
                        'CORPUS_PATH': f'..{self.dataset.data_path}'
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
        # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/segments {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/text {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/utt2spk {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/testing/wav.scp {{ .KALDI_OUTPUT_PATH }}/kaldi/data/test/
        shutil.move(f"{output_path.joinpath('testing', 'segments')}", f"{kaldi_data_test.joinpath('segments')}")
        shutil.move(f"{output_path.joinpath('testing', 'text')}", f"{kaldi_data_test.joinpath('text')}")
        shutil.move(f"{output_path.joinpath('testing', 'utt2spk')}", f"{kaldi_data_test.joinpath('utt2spk')}")
        shutil.move(f"{output_path.joinpath('testing', 'wav.scp')}", f"{kaldi_data_test.joinpath('wav.scp')}")
        # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/segments {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/text {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/utt2spk {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/wav.scp {{ .KALDI_OUTPUT_PATH }}/kaldi/data/train/
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
        shutil.copy(f"{template_path.joinpath('run.sh')}", f"{local_kaldi_path}")
        # - cp {{ .KALDI_TEMPLATES }}/score.sh {{ .KALDI_OUTPUT_PATH }}/kaldi/local/
        shutil.copy(f"{template_path.joinpath('score.sh')}", f"{kaldi_local}")
        # - cp -L -r {{ .KALDI_ROOT }}/egs/wsj/s5/steps {{ .KALDI_OUTPUT_PATH }}/kaldi/steps
        p = run(f"cp -L -r /kaldi/egs/wsj/s5/steps {local_kaldi_path}/steps")
        # - cp -L -r {{ .KALDI_ROOT }}/egs/wsj/s5/utils {{ .KALDI_OUTPUT_PATH }}/kaldi/utils
        p = run(f"cp -L -r /kaldi/egs/wsj/s5/utils {local_kaldi_path}/utils")

        # modified extract-wavs
        for audio_file in os.listdir(self.dataset.resampled_path):
            src = f'{self.dataset.resampled_path.joinpath(audio_file)}'
            dst=f'{local_kaldi_path}'
            shutil.copy(src, dst)
        print('done.')


        # Setup for Training complete
        ######################################################################

        # task _test-train
        p = run(f"cd {local_kaldi_path}; ./run.sh")
        print(p.stdout)
        print('double done.')

        return