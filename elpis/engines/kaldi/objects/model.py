from loguru import logger
import os
import re
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
from subprocess import CalledProcessError
from jinja2 import Template


class KaldiModel(BaseModel):  # TODO not thread safe
    # _links = {**Model._links, **{"pron_dict": PronDict}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pron_dict: PronDict = None
        self.config["pron_dict_name"] = None  # pron_dict hash has not been linked
        self.config["engine_name"] = "kaldi"
        stage_names = {
            "0_setup.sh": "setup",
            "1_prep_acoustic.sh": "acousticPreparation",
            "2_feature_ext.sh": "featureExtraction",
            "3_prep_lang_data.sh": "dataPreparation",
            "4_lang_model_cr.sh": "modelCreation",
            "5_mono.sh": "monophoneTraining",
            "6_tri1.sh": "triphoneTraining",
        }
        super().build_stage_status(stage_names)
        self.status = "untrained"
        self.config["stage_count"] = 0
        self.config["current_stage"] = "0_setup.sh"
        self.settings = {"ngram": 1}
        logger.info(f"model default settings {self.settings}")
        self.run_log_path = self.path.joinpath("train.log")
        self.config["run_log_path"] = self.run_log_path.as_posix()
        if not Path(self.run_log_path).is_file():
            run(f"touch {self.run_log_path};")
        logger.add(self.run_log_path)

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        logger.info(f"load {base_path}")
        self.pron_dict = None
        return self

    @property
    def log(self):
        with open(self.config["run_log_path"]) as logs:
            return logs.read()

    def link_pron_dict(self, pron_dict: PronDict):
        self.pron_dict = pron_dict
        self.config["pron_dict_name"] = pron_dict.name

    def build_structure(self):
        # task json-to-kaldi
        output_path = self.path.joinpath("output")
        output_path.mkdir(parents=True, exist_ok=True)

        # Copy cleaned corpus from dataset to the model
        dataset_corpus_txt = self.dataset.path.joinpath("cleaned", "corpus.txt")
        model_corpus_txt = self.path.joinpath("corpus.txt")
        if dataset_corpus_txt.exists():
            shutil.copy(f"{dataset_corpus_txt}", f"{model_corpus_txt}")
        create_kaldi_structure(
            input_json=f"{self.dataset.pathto.annotation_json}",
            output_folder=f"{output_path}",
            silence_markers=False,
            corpus_txt=f"{model_corpus_txt}",
        )

    def train(self, on_complete: Callable = None):
        def prepare_for_training():
            logger.info("prepare_for_training")
            # task make-kaldi-subfolders
            kaldi_structure = PathStructure(self.path)

            local_kaldi_path = self.path.joinpath("kaldi")
            local_kaldi_path.mkdir(parents=True, exist_ok=True)
            kaldi_data_local_dict = local_kaldi_path.joinpath("data", "local", "dict")
            kaldi_data_local_dict.mkdir(parents=True, exist_ok=True)
            kaldi_data_local = local_kaldi_path.joinpath("data", "local")
            kaldi_data_local.mkdir(parents=True, exist_ok=True)
            kaldi_data_test = local_kaldi_path.joinpath("data", "test")
            kaldi_data_test.mkdir(parents=True, exist_ok=True)
            kaldi_data_train = local_kaldi_path.joinpath("data", "train")
            kaldi_data_train.mkdir(parents=True, exist_ok=True)
            kaldi_conf = local_kaldi_path.joinpath("conf")
            kaldi_conf.mkdir(parents=True, exist_ok=True)
            kaldi_local = local_kaldi_path.joinpath("local")
            kaldi_local.mkdir(parents=True, exist_ok=True)

            # copy the pron dict
            shutil.copy(
                f"{self.pron_dict.lexicon_txt_path}",
                f"{kaldi_data_local_dict.joinpath('lexicon.txt')}",
            )

            # task generate-kaldi-configs
            path_file_path = kaldi_structure.path.joinpath("path.sh")
            mfcc_file_path = kaldi_structure.conf.joinpath("mfcc.conf")
            decode_config_file_path = kaldi_structure.conf.joinpath("decode.config")

            template_path = Path("/elpis/elpis/engines/kaldi/templates")
            path_resource = template_path.joinpath("path.sh")
            mfcc_resource = template_path.joinpath("mfcc.conf")
            decode_config_resource = template_path.joinpath("decode.config")

            # task make-nonsil-phones > {{ .KALDI_OUTPUT_PATH }}/tmp/nonsilence_phones.txt
            nonsilence_phones_path = kaldi_data_local_dict.joinpath("nonsilence_phones.txt")
            # build a unique non-sorted list of the phone symbols
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
            with nonsilence_phones_path.open(mode="w") as fout:
                for (item, i) in seen.items():
                    fout.write("%s\n" % item)

            with path_file_path.open(mode="w") as fout:
                with path_resource.open() as fin:
                    content = Template(fin.read()).render(
                        {
                            "KALDI_ROOT": "/kaldi",
                            "HELPERS_PATH": "/kaldi-helpers",
                            "CORPUS_PATH": f"..{self.dataset.pathto.original}",
                        }
                    )
                    fout.write(content)

            with mfcc_file_path.open(mode="w") as fout:
                with mfcc_resource.open() as fin:
                    content = Template(fin.read()).render(
                        {
                            "MFCC_SAMPLE_FREQUENCY": "16000",
                            "MFCC_FRAME_LENGTH": "25",
                            "MFCC_LOW_FREQ": "20",
                            "MFCC_HIGH_FREQ": "7800",
                            "MFCC_NUM_CEPS": "7",
                        }
                    )
                    fout.write(content)

            with decode_config_file_path.open(mode="w") as fout:
                with decode_config_resource.open() as fin:
                    content = Template(fin.read()).render(
                        {"DECODE_BEAM": "11.0", "DECODE_FIRST_BEAM": "8.0"}
                    )
                    fout.write(content)
            try:
                # task copy-generated-files
                output_path = self.path.joinpath("output")
                output_path.mkdir(parents=True, exist_ok=True)

                # - cp {{ .KALDI_OUTPUT_PATH }}/tmp/json_splitted/training/corpus.txt {{ .KALDI_OUTPUT_PATH }}/kaldi/data/local/
                shutil.move(
                    f"{output_path.joinpath('training', 'corpus.txt')}", f"{kaldi_data_local}"
                )
                shutil.move(
                    f"{output_path.joinpath('testing', 'segments')}",
                    f"{kaldi_data_test.joinpath('segments')}",
                )
                shutil.move(
                    f"{output_path.joinpath('testing', 'text')}",
                    f"{kaldi_data_test.joinpath('text')}",
                )
                shutil.move(
                    f"{output_path.joinpath('testing', 'utt2spk')}",
                    f"{kaldi_data_test.joinpath('utt2spk')}",
                )
                shutil.move(
                    f"{output_path.joinpath('testing', 'wav.scp')}",
                    f"{kaldi_data_test.joinpath('wav.scp')}",
                )
                shutil.move(
                    f"{output_path.joinpath('training', 'segments')}",
                    f"{kaldi_data_train.joinpath('segments')}",
                )
                shutil.move(
                    f"{output_path.joinpath('training', 'text')}",
                    f"{kaldi_data_train.joinpath('text')}",
                )
                shutil.move(
                    f"{output_path.joinpath('training', 'utt2spk')}",
                    f"{kaldi_data_train.joinpath('utt2spk')}",
                )
                shutil.move(
                    f"{output_path.joinpath('training', 'wav.scp')}",
                    f"{kaldi_data_train.joinpath('wav.scp')}",
                )

                # task copy-phones-configs
                optional_silence_file_path = kaldi_data_local_dict.joinpath("optional_silence.txt")
                silence_phones_file_path = kaldi_data_local_dict.joinpath("silence_phones.txt")
                with optional_silence_file_path.open(mode="w") as fout:
                    fout.write("SIL\n")
                with silence_phones_file_path.open(mode="w") as fout:
                    fout.write("SIL\nsil\nspn\n")

                shutil.copy(f"{template_path.joinpath('cmd.sh')}", f"{local_kaldi_path}")
                shutil.copytree(
                    f"{template_path.joinpath('stages')}", local_kaldi_path.joinpath("stages")
                )
                for file in os.listdir(local_kaldi_path.joinpath("stages")):
                    os.chmod(local_kaldi_path.joinpath("stages").joinpath(file), 0o774)

                shutil.copy(f"{template_path.joinpath('score.sh')}", f"{kaldi_local}")
                run(f"cp -L -r /kaldi/egs/wsj/s5/steps {local_kaldi_path}/steps")
                run(f"cp -L -r /kaldi/egs/wsj/s5/utils {local_kaldi_path}/utils")

                # modified extract-wavs
                for audio_file in os.listdir(self.dataset.pathto.resampled):
                    src = f"{self.dataset.pathto.resampled.joinpath(audio_file)}"
                    dst = f"{local_kaldi_path}"
                    shutil.copy(src, dst)
                logger.info("kaldi dirs preparation done.")
            except OSError as error:
                logger.error("couldnt prepare kaldi dirs: ", error)

        def train():
            local_kaldi_path = self.path.joinpath("kaldi")

            self.config["stage_count"] = 0
            stages = os.listdir(local_kaldi_path.joinpath("stages"))

            for stage in sorted(stages):
                logger.info(f"Stage {stage} starting")
                self.stage_status = (stage, "in-progress")
                self.config["current_stage"] = stage

                # TODO update stage templates with jinja templates or something similar
                with open(local_kaldi_path.joinpath("stages").joinpath(stage), "r") as file:
                    filedata = file.read()
                # Add settings to replace here
                filedata = filedata.replace("lm_order=1", f'lm_order={self.settings["ngram"]}')
                with open(local_kaldi_path.joinpath("stages").joinpath(stage), "w") as file:
                    file.write(filedata)

                # Run the command, log output. Also redirect Kaldi sterr output to log. These are often not errors :-(
                try:
                    run(f"cd {local_kaldi_path}; stages/{stage} >> {self.run_log_path}")
                    logger.info(f"Stage {stage} complete")
                    self.stage_status = (stage, "complete")
                    self.config["stage_count"] = self.config["stage_count"] + 1
                except CalledProcessError as error:
                    with open(self.run_log_path, "a+") as file:
                        print("stderr", error.stderr, file=file)
                        print("failed", file=file)
                    logger.error(f"Stage {stage} failed")
                    self.stage_status = (stage, "failed")
                    break

        def run_training_in_background():
            def background_train_task():
                prepare_for_training()
                train()
                self.status = "trained"
                self.results = KaldiModel.get_train_results(self)
                on_complete()

            self.status = "training"
            t = threading.Thread(target=background_train_task)
            t.start()

        if on_complete is None:
            self.status = "training"
            prepare_for_training()
            train()
            self.status = "trained"
            self.results = KaldiModel.get_train_results(self)
        else:
            run_training_in_background()
        return

    def get_train_results(self):
        results = {}
        if Path(self.config["run_log_path"]).exists():
            with Path(self.config["run_log_path"]).open() as log_file:
                wer_lines = []
                for line in reversed(list(log_file)):
                    line = line.rstrip()
                    if "%WER" in line:
                        # use line to sort by best val
                        line_r = line.replace("%WER ", "")
                        wer_lines.append(line_r)
                if len(wer_lines) > 0:
                    wer_lines.sort(reverse=True)
                    line = wer_lines[0]
                    line_split = line.split(None, 1)
                    wer = line_split[0]
                    line_results = line_split[1]
                    line_results = re.sub("[\[\]]", "", line_results)
                    results_split = line_results.split(",")
                    count_val = results_split[0].strip()
                    ins_val = results_split[1].replace(" ins", "").strip()
                    del_val = results_split[2].replace(" del", "").strip()
                    sub_val = results_split[3].replace(" sub", "").strip()
                    results = {
                        "comparison_val": float(
                            wer
                        ),  # common for all engines so GUI can sort by a result value
                        "wer": float(wer),
                        "count_val": str(count_val),
                        "ins_val": int(ins_val),
                        "del_val": int(del_val),
                        "sub_val": int(sub_val),
                    }
                    print(results)
        return results
