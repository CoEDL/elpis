import pytest
import os
import shutil
import hashlib
from .. import paths
from . import model, KaldiError

def _clear_models_dir():
    # empty the models directory
    if os.path.exists(paths.MODELS_DIR):
        shutil.rmtree(paths.MODELS_DIR)
    os.mkdir(paths.MODELS_DIR)

def test_get_list():
    _clear_models_dir()
    # add stub models
    os.mkdir(paths.MODELS_DIR + '/m1')
    with open(paths.MODELS_DIR + '/m1/name.txt', 'w') as fout:
        fout.write('carlos')
    os.mkdir(paths.MODELS_DIR + '/m2')
    with open(paths.MODELS_DIR + '/m2/name.txt', 'w') as fout:
        fout.write('dallis')
    os.mkdir(paths.MODELS_DIR + '/m3')
    with open(paths.MODELS_DIR + '/m3/name.txt', 'w') as fout:
        fout.write('other nic')
    # Test the results
    names = model.get_list()
    assert 'carlos' in names
    assert 'other nic' in names
    assert 'dallis' in names

def test_new():
    _clear_models_dir()
    model.new('daffy duck')
    d = hashlib.md5(b'daffy duck').hexdigest()
    with open(f'{paths.MODELS_DIR}/{d}/name.txt', 'r') as fin:
        name = fin.read()
    assert name == 'daffy duck'
    

def test_new_model_already_exists():
    _clear_models_dir()
    print(f'model.new: {model.new}')
    print(f'model.new.f: {model.new.f}')
    with pytest.raises(KaldiError) as error:
        model.new('bugs bunny')
        model.new('bugs bunny')
    assert 'model already exists with the name: \'bugs bunny\'' == str(error.value)

def test_new_invalid_name():
    _clear_models_dir()
    with pytest.raises(KaldiError) as error:
        model.new('')
    assert 'invalid model name: \'\'' == str(error.value)
