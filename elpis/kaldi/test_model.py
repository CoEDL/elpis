import pytest
import os
import shutil
import hashlib
from .. import paths
from . import model, KaldiError

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
    if os.path.exists(paths.CURRENT_MODEL_DIR):
        shutil.rmtree(paths.CURRENT_MODEL_DIR)
    os.mkdir(paths.CURRENT_MODEL_DIR)

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

##############################################################################
#                           Let the testing begin!                           #
##############################################################################

def test__get_status_no_dir():
    # remove model dir
    if os.path.exists(paths.CURRENT_MODEL_DIR):
        shutil.rmtree(paths.CURRENT_MODEL_DIR)
    assert model._get_status(paths.CURRENT_MODEL_DIR) == 'No Model'

def test__get_status_empty_dir():
    # empty model dir
    _clear_model_dir()
    assert model._get_status(paths.CURRENT_MODEL_DIR) == 'No Model'

def test__get_status_after_new_model():
    _clear_model_dir()
    _touch(f'{paths.CURRENT_MODEL_DIR}/name.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/date.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/hash.txt')
    assert model._get_status(paths.CURRENT_MODEL_DIR) == 'Incomplete Model'

def test__get_status_after_add_data():
    _clear_model_dir()
    _touch(f'{paths.CURRENT_MODEL_DIR}/name.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/date.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/hash.txt')
    os.mkdir(f'{paths.CURRENT_MODEL_DIR}/data')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f1.eaf')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f1.wav')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f2.eaf')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f2.wav')
    assert model._get_status(paths.CURRENT_MODEL_DIR) == 'Incomplete Model'

def test__get_status_after_load_pron_dict():
    _clear_model_dir()
    _touch(f'{paths.CURRENT_MODEL_DIR}/name.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/date.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/hash.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/wordlist.json')
    os.mkdir(f'{paths.CURRENT_MODEL_DIR}/data')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f1.eaf')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f1.wav')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f2.eaf')
    _touch(f'{paths.CURRENT_MODEL_DIR}/data/f2.wav')
    os.mkdir(f'{paths.CURRENT_MODEL_DIR}/config')
    _touch(f'{paths.CURRENT_MODEL_DIR}/config/letter_to_sound.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/config/optional_silence.txt')
    _touch(f'{paths.CURRENT_MODEL_DIR}/config/silence_phones.txt')
    assert model._get_status(paths.CURRENT_MODEL_DIR) == 'Untrained Model'

def test__get_status_after_load_pron_dict_and_get_word_list():
    # TODO same as test__get_status_after_load_pron_dict but with the word list tiles as well -> 'Untrained Model'
    pass

def test_load_transcription_files():
    _clear_model_dir()
    os.mkdir(f'{paths.CURRENT_MODEL_DIR}/data')
    model.load_transcription_files([
        (('f1.eaf', b'a'), ('f1.wav', b'b')),
        (('f2.eaf', b'c'), ('f2.wav', b'd'))
    ])
    with open(f'{paths.CURRENT_MODEL_DIR}/data/f1.eaf', 'rb') as f1e:
        assert f1e.read() == b'a'
    with open(f'{paths.CURRENT_MODEL_DIR}/data/f1.wav', 'rb') as f1w:
        assert f1w.read() == b'b'
    with open(f'{paths.CURRENT_MODEL_DIR}/data/f2.eaf', 'rb') as f2e:
        assert f2e.read() == b'c'
    with open(f'{paths.CURRENT_MODEL_DIR}/data/f2.wav', 'rb') as f2w:
        assert f2w.read() == b'd'

def test_generate_word_list():
    _clear_kaldi_model_dir()
    _clear_model_dir()
    model.new('arctic')
    shutil.copytree(f'{paths.ELPIS_ROOT_DIR}/abui_toy_corpus/data', f'{paths.CURRENT_MODEL_DIR}/data')
    model._sync_to_kaldi()
    model.generate_word_list()
    assert os.path.exists(f'{paths.CURRENT_MODEL_DIR}/wordlist.json')
