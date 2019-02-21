import os
import shlex
import subprocess
from shutil import copytree
from elpis.blueprint import Blueprint
from elpis.paths import CURRENT_MODEL_DIR
from elpis import kaldi


bp = Blueprint("kaldi", __name__, url_prefix="/kaldi")


def log(content: str):
    log_path = os.path.join(CURRENT_MODEL_DIR, 'log.txt')
    with open(log_path, 'w+') as fout:
        fout.write(content)


def run_to_log(cmd: str) -> str:
    """Captures stdout/stderr and writes it to a log file, then returns the
    CompleteProcess result object"""
    args = shlex.split(cmd)
    process = subprocess.run(
        args,
        check=True,
        cwd='/kaldi-helpers',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    log(process.stdout.decode("utf-8"))
    return process


def ensure_exists(dir: str):
    if os.path.exists(dir):
        return
    run_to_log(f'mkdir -p { dir }')


INPUT_PATH = ""


class KaldiModelBridge(object):
    """

    """
    status = None

    @classmethod
    def new(cls):
        print(f'want to clear the floor')
        return run_to_log(f'rm -rf {CURRENT_MODEL_DIR}/*').stdout


class KaldiTranscriptionBridge(object):

    @classmethod
    def new(cls):
        pass

    @classmethod
    def transcribe(cls):
        pass

    @classmethod
    def transcribe_align(cls):
        pass


@bp.route('/new')
def new():
    kaldi.Bridge.task('new-model', cwd='/elpis')

    return ''


@bp.route('/run-elan')
def run_elan():
    kaldi.Bridge.task('transfer-model-to-kaldi', cwd='/elpis')
    process = kaldi.run_elan()
    return process.stdout


@bp.route('/train')
def train():
    process = kaldi.train()
    return process.stdout


@bp.route('/transcribe')
def transcribe():
    # KALDI_OUTPUT_PATH = '/kaldi-helpers/working_dir/input/output'
    # # ensure_exists(f'{ KALDI_OUTPUT_PATH }/kaldi/data/infer')
    # run_to_log(f'rm -rf { KALDI_OUTPUT_PATH }/kaldi/data/infer')
    # copytree(f'{ KALDI_OUTPUT_PATH }/kaldi/data/test/',
    #          f'{ KALDI_OUTPUT_PATH }/kaldi/data/infer')
    # log(f'cp -R { KALDI_OUTPUT_PATH }/kaldi/data/test/ { KALDI_OUTPUT_PATH }/kaldi/data/infer')
    # ensure_exists('/kaldi-helpers/working_dir/input/infer')
    process = kaldi.transcribe()
    return process.stdout


@bp.route('/transcribe-align')
def transcribe_align():
    KALDI_OUTPUT_PATH = '/kaldi-helpers/working_dir/input/output'
    # ensure_exists(f'{ KALDI_OUTPUT_PATH }/kaldi/data/infer')
    run_to_log(f'rm -rf { KALDI_OUTPUT_PATH }/kaldi/data/infer')
    copytree(f'{ KALDI_OUTPUT_PATH }/kaldi/data/test/',
             f'{ KALDI_OUTPUT_PATH }/kaldi/data/infer')
    ensure_exists('/kaldi-helpers/working_dir/input/infer')
    process = run_to_log('task infer-align')
    return process.stdout

@bp.route('/q')
def q():
    process = kaldi.Bridge.task('transfer-model-to-kaldi', cwd='/elpis')
    return process.stdout
