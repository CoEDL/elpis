import pystache
import os
import shutil
from pathlib import Path
from typing import Callable, Dict, Tuple
import threading
from elpis.engines.common.objects.command import run
from elpis.engines.common.objects.model import Model as BaseModel
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.pron_dict import PronDict
from elpis.engines.kaldi.input.json_to_kaldi import create_kaldi_structure
from elpis.engines.common.objects.path_structure import PathStructure
from collections import OrderedDict


class KaldiModel(BaseModel):  # TODO not thread safe
    # _links = {**Model._links, **{"pron_dict": PronDict}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pron_dict: PronDict = None
        self.config['pron_dict_name'] = None  # pron_dict hash has not been linked
        self.config['ngram'] = 1  # default to 1 to make playing quicker
        stage_names = {
            "0_setup.sh": "Set up",
            "1_prep_acoustic.sh": "Prepare acoustic data",
            "2_feature_ext.sh": "Extract features",
            "3_prep_lang_data.sh": "Prepare language data",
            "4_lang_model_cr.sh": "Create language model",
            "5_mono.sh": "Monophone training",
            "6_tri1.sh": "Triphone training"
        }
        super().build_stage_status(stage_names)

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pron_dict = None
        return self
    
    @property
    def state(self):
        # TODO: fix this
        return {}

    def has_been_trained(self):
        return self.status == 'trained'

    def link_pron_dict(self, pron_dict: PronDict):
        print("**** linking Kaldi model with pron dict")
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
        
        # Copy cleaned corpus from dataset to the model
        dataset_corpus_txt = self.dataset.path.joinpath('cleaned', 'corpus.txt')
        model_corpus_txt = self.path.joinpath('corpus.txt')
        if os.path.exists(dataset_corpus_txt):
            shutil.copy(f"{dataset_corpus_txt}", f"{model_corpus_txt}")
        create_kaldi_structure(
            input_json=f'{self.dataset.pathto.annotation_json}',
            output_folder=f'{output_path}',
            silence_markers=False,
            corpus_txt=f'{model_corpus_txt}'
        )

    def train(self, on_complete:Callable=None):

        def prepare_for_training():
            print("prepare_for_training")
            # task make-kaldi-subfolders
            kaldi_structure = PathStructure(self.path)

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
            shutil.copy(f"{self.pron_dict.lexicon_txt_path}", f"{kaldi_data_local_dict.joinpath('lexicon.txt')}")

            # task generate-kaldi-configs
            path_file_path = kaldi_structure.path.joinpath('path.sh')
            mfcc_file_path = kaldi_structure.conf.joinpath('mfcc.conf')
            decode_config_file_path = kaldi_structure.conf.joinpath('decode.config')

            template_path = Path('/elpis/elpis/engines/kaldi/templates')
            path_resource = template_path.joinpath('path.sh')
            mfcc_resource = template_path.joinpath('mfcc.conf')
            decode_config_resource = template_path.joinpath('decode.config')

            # task make-nonsil-phones > {{ .KALDI_OUTPUT_PATH }}/tmp/nonsilence_phones.txt
            nonsilence_phones_path = kaldi_data_local_dict.joinpath('nonsilence_phones.txt')
            # build a unnique non-sorted list of the phone symbols
            # can't use sorting, because the rules may have order significance
            # ignore comment lines that begin with #
            seen = OrderedDict()
            for line in open(self.pron_dict.l2s_path, "r"):
                if line[0] == "#":
                    pass
                else:
                    line = line.split()[1:]
                    if len(line) > 0:
                        line = line[0]
                        seen[line] = seen.get(line, 0) + 1
            with nonsilence_phones_path.open(mode='w') as fout:
                for (item, i) in seen.items():
                    fout.write("%s\n" % item)

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
                shutil.move(f"{output_path.joinpath('testing', 'segments')}", f"{kaldi_data_test.joinpath('segments')}")
                shutil.move(f"{output_path.joinpath('testing', 'text')}", f"{kaldi_data_test.joinpath('text')}")
                shutil.move(f"{output_path.joinpath('testing', 'utt2spk')}", f"{kaldi_data_test.joinpath('utt2spk')}")
                shutil.move(f"{output_path.joinpath('testing', 'wav.scp')}", f"{kaldi_data_test.joinpath('wav.scp')}")
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

                shutil.copy(f"{template_path.joinpath('cmd.sh')}", f"{local_kaldi_path}")
                shutil.copytree(f"{template_path.joinpath('stages')}", local_kaldi_path.joinpath('stages'))
                for file in os.listdir(local_kaldi_path.joinpath('stages')):
                    os.chmod(local_kaldi_path.joinpath('stages').joinpath(file), 0o774)

                shutil.copy(f"{template_path.joinpath('score.sh')}", f"{kaldi_local}")
                run(f"cp -L -r /kaldi/egs/wsj/s5/steps {local_kaldi_path}/steps")
                run(f"cp -L -r /kaldi/egs/wsj/s5/utils {local_kaldi_path}/utils")

                # modified extract-wavs
                for audio_file in os.listdir(self.dataset.pathto.resampled):
                    src = f'{self.dataset.pathto.resampled.joinpath(audio_file)}'
                    dst = f'{local_kaldi_path}'
                    shutil.copy(src, dst)
                print('kaldi dirs preparation done.')
            except OSError as error:
                print('couldnt prepare kaldi dirs: ', error)

        def train():
            local_kaldi_path = self.path.joinpath('kaldi')

            # Setup for Training complete
            ######################################################################

            # task _test-train
            run_log_path = self.path.joinpath('train.log')
            if os.path.isfile(run_log_path):
                os.remove(run_log_path)
            stages = os.listdir(local_kaldi_path.joinpath('stages'))
            run(f"touch {run_log_path};")
            for stage in sorted(stages):
                print(f"======== STAGE {stage} STARTING ========")
                self.stage_status = (stage, 'in-progress', '')
                
                with open(local_kaldi_path.joinpath('stages').joinpath(stage), 'r') as file :
                    filedata = file.read()

                filedata = filedata.replace('lm_order=1', f'lm_order={self.ngram}')

                with open(local_kaldi_path.joinpath('stages').joinpath(stage), 'w') as file:
                    file.write(filedata)
                p = run(f"cd {local_kaldi_path}; stages/{stage} >> {run_log_path}")
                print(p.stdout)
                print(f"======== STAGE {stage} COMPLETE ========")
                self.stage_status = (stage, 'complete', '')

            self.log = run(f"cd {local_kaldi_path}; cat {run_log_path}").stdout
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
