import pytest
import os
import shutil
from . import KaldiError
from .fsobject import FileSystemObject

##############################################################################
#                              Utility functions                             #
##############################################################################

path_working = './test_object_working'
path_save = './test_object_save'
path_kaldi = './test_object_kaldi'

def _clear_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def _clear_working_dir():
    _clear_dir(path_working)

def _clear_save_dir():
    _clear_dir(path_save)

def _clear_kaldi_dir():
    _clear_dir(path_kaldi)

def _touch(path):
    contents = ''
    if os.path.exists(path):
        with open(path, 'r') as fin:
            contents = fin.read()
    with open(path, 'w') as fout:
        fout.write(contents)

model = FileSystemObject(path_working, path_save, path_kaldi)

##############################################################################
#                           Let the testing begin!                           #
##############################################################################

def test_new():
    _clear_working_dir()
    _clear_save_dir()
    model.new('daffy duck')
    with open(f'{path_working}/name.txt', 'r') as fin:
        name = fin.read()
    assert name == 'daffy duck'
    assert os.path.exists(f'{path_working}/date.txt')
    assert os.path.exists(f'{path_working}/hash.txt')

def test_sync_to_kaldi():
    _clear_working_dir()
    _clear_kaldi_dir()
    _touch(f'{path_working}/sync')
    assert not os.path.exists(f'{path_kaldi}/sync')
    model.sync_to_kaldi()
    assert os.path.exists(f'{path_kaldi}/sync')

def test_sync_to_working():
    _clear_working_dir()
    _clear_kaldi_dir()
    _touch(f'{path_kaldi}/sync')
    assert not os.path.exists(f'{path_working}/sync')
    model.sync_to_working()
    assert os.path.exists(f'{path_working}/sync')

def test_get_list():
    _clear_save_dir()
    # add stub models
    os.mkdir(path_save + '/m1')
    with open(path_save + '/m1/name.txt', 'w') as fout:
        fout.write('carlos')
    os.mkdir(path_save + '/m2')
    with open(path_save + '/m2/name.txt', 'w') as fout:
        fout.write('dallis')
    os.mkdir(path_save + '/m3')
    with open(path_save + '/m3/name.txt', 'w') as fout:
        fout.write('other nic')
    # Test the results
    names = model.get_list()
    assert 'carlos' in names
    assert 'other nic' in names
    assert 'dallis' in names

def test_new_model_already_exists():
    _clear_save_dir()
    _clear_working_dir()
    os.mkdir(path_save + '/m')
    with open(path_save + '/m/name.txt', 'w') as fout:
        fout.write('bugs bunny')
    with pytest.raises(KaldiError) as error:
        model.new('bugs bunny')
    assert 'model already exists with the name: \'bugs bunny\'' == str(error.value)

def test_new_invalid_name():
    _clear_working_dir()
    with pytest.raises(KaldiError) as error:
        model.new('')
    assert 'invalid model name: \'\'' == str(error.value)


def test_new_with_sync():
    _clear_working_dir()
    _clear_kaldi_dir()
    model.new('nildocaafiat')
    namefile = f'{path_kaldi}/name.txt'
    assert os.path.exists(namefile)
    with open(namefile, 'r') as fin:
        assert fin.read() == 'nildocaafiat'

def test_get_name():
    _clear_working_dir()
    _clear_kaldi_dir()
    model.new('nildocaafiat')
    assert model.get_name() == 'nildocaafiat'

def test_get_date():
    _clear_working_dir()
    _clear_kaldi_dir()
    model.new('nildocaafiat')
    assert model.get_date() > 1

def test_get_hash():
    _clear_working_dir()
    _clear_kaldi_dir()
    model.new('nildocaafiat')
    allowed_chars = set('abcdefABCDEF0123456789')
    assert set(model.get_hash()).issubset(allowed_chars)