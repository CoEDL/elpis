import pytest
import os
import shutil
import hashlib
from .. import paths
from . import KaldiError
from .model import Model

##############################################################################
#                              Utility functions                             #
##############################################################################

def _clear_models_dir():
    # empty the models directory
    if os.path.exists(paths.MODELS_DIR):
        shutil.rmtree(paths.MODELS_DIR)
    os.mkdir(paths.MODELS_DIR)

def _clear_model_dir():
    # empty the current model directory
    if os.path.exists(path_working):
        shutil.rmtree(path_working)
    os.mkdir(path_working)

def _clear_kaldi_model_dir():
    if os.path.exists(paths.kaldi_helpers.INPUT_PATH):
        shutil.rmtree(paths.kaldi_helpers.INPUT_PATH)
    os.mkdir(paths.kaldi_helpers.INPUT_PATH)

def _touch(path):
    contents = ''
    if os.path.exists(path):
        with open(path, 'r') as fin:
            contents = fin.read()
    with open(path, 'w') as fout:
        fout.write(contents)

path_working = paths.CURRENT_MODEL_DIR
path_save = paths.MODELS_DIR
path_kaldi = paths.kaldi_helpers.INPUT_PATH

model = Model('model', path_working, path_save, path_kaldi)

##############################################################################
#                           Let the testing begin!                           #
##############################################################################

def test__get_status_no_dir():
    # remove model dir
    if os.path.exists(path_working):
        shutil.rmtree(path_working)
    assert model.get_status(path_working) == 'No Model'

def test__get_status_empty_dir():
    # empty model dir
    _clear_model_dir()
    assert model.get_status(path_working) == 'No Model'

def test__get_status_after_new_model():
    _clear_model_dir()
    _touch(f'{path_working}/name.txt')
    _touch(f'{path_working}/date.txt')
    _touch(f'{path_working}/hash.txt')
    assert model.get_status(path_working) == 'Incomplete Model'

def test__get_status_after_add_data():
    _clear_model_dir()
    _touch(f'{path_working}/name.txt')
    _touch(f'{path_working}/date.txt')
    _touch(f'{path_working}/hash.txt')
    os.mkdir(f'{path_working}/data')
    _touch(f'{path_working}/data/f1.eaf')
    _touch(f'{path_working}/data/f1.wav')
    _touch(f'{path_working}/data/f2.eaf')
    _touch(f'{path_working}/data/f2.wav')
    assert model.get_status(path_working) == 'Incomplete Model'

def test__get_status_after_load_pron_dict():
    _clear_model_dir()
    _touch(f'{path_working}/name.txt')
    _touch(f'{path_working}/date.txt')
    _touch(f'{path_working}/hash.txt')
    _touch(f'{path_working}/wordlist.json')
    os.mkdir(f'{path_working}/data')
    _touch(f'{path_working}/data/f1.eaf')
    _touch(f'{path_working}/data/f1.wav')
    _touch(f'{path_working}/data/f2.eaf')
    _touch(f'{path_working}/data/f2.wav')
    os.mkdir(f'{path_working}/config')
    _touch(f'{path_working}/config/letter_to_sound.txt')
    _touch(f'{path_working}/config/optional_silence.txt')
    _touch(f'{path_working}/config/silence_phones.txt')
    assert model.get_status(path_working) == 'Untrained Model'

def test__get_status_after_load_pron_dict_and_get_word_list():
    # TODO same as test__get_status_after_load_pron_dict but with the word list tiles as well -> 'Untrained Model'
    pass

def test_load_transcription_files():
    _clear_model_dir()
    os.mkdir(f'{path_working}/data')
    model.load_transcription_files([
        (('f1.eaf', b'a'), ('f1.wav', b'b')),
        (('f2.eaf', b'c'), ('f2.wav', b'd'))
    ])
    with open(f'{path_working}/data/f1.eaf', 'rb') as f1e:
        assert f1e.read() == b'a'
    with open(f'{path_working}/data/f1.wav', 'rb') as f1w:
        assert f1w.read() == b'b'
    with open(f'{path_working}/data/f2.eaf', 'rb') as f2e:
        assert f2e.read() == b'c'
    with open(f'{path_working}/data/f2.wav', 'rb') as f2w:
        assert f2w.read() == b'd'

def test_generate_word_list():
    _clear_kaldi_model_dir()
    _clear_model_dir()
    model.new('arctic')
    shutil.copytree(f'{paths.ELPIS_ROOT_DIR}/abui_toy_corpus/data', f'{path_working}/data')
    model.sync_to_kaldi()
    model.generate_word_list()
    assert os.path.exists(f'{path_working}/wordlist.json')
