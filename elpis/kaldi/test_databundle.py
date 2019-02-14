import pytest
import os
import shutil
from .. import paths
from . import KaldiError
from .databundle import DataBundle


path_working = './test_object_db_working'
path_save = './test_object_db_save'
path_kaldi = paths.kaldi_helpers.INPUT_PATH
path_toy = os.path.join(paths.ELPIS_ROOT_DIR, 'abui_toy_corpus', 'data')

db = DataBundle('data bundle', path_working, path_save, path_kaldi)

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

def test_adding_data():
    _clear_working_dir()
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin, name='this.eaf')
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin, name='this.wav')
    assert os.path.exists(f'{path_kaldi}/data/this.eaf')
    assert os.path.exists(f'{path_kaldi}/data/this.wav')

def test_adding_data_no_name():
    _clear_working_dir()
    _clear_kaldi_dir()
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin)
    assert os.path.exists(f'{path_kaldi}/data/1_1_1.eaf')
    assert os.path.exists(f'{path_kaldi}/data/1_1_1.wav')

def test_prepare():
    _clear_working_dir()
    _clear_kaldi_dir()
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin)
    db.prepare()
    assert os.path.exists(f'{path_working}/wordlist.json')

