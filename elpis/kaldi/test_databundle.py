import pytest
import os
import shutil
from .. import paths
from .errors import KaldiError
from .databundle import DataBundle
from .test_util import Context

path_toy = os.path.join(paths.ELPIS_ROOT_DIR, 'abui_toy_corpus', 'data')

# db = DataBundle('data bundle', path_working, path_save, path_kaldi)
ctx = Context(DataBundle, 'data bundle')
ctx.path_kaldi = paths.kaldi_helpers.INPUT_PATH

@ctx
def test_adding_data(db: DataBundle):
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin, name='this.eaf')
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin, name='this.wav')
    assert os.path.exists(f'{ctx.path_kaldi}/this.eaf')
    assert os.path.exists(f'{ctx.path_kaldi}/this.wav')

@ctx
def test_adding_data_no_name(db: DataBundle):
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin)
    assert os.path.exists(f'{ctx.path_kaldi}/1_1_1.eaf')
    assert os.path.exists(f'{ctx.path_kaldi}/1_1_1.wav')

@ctx
def test_prepare(db: DataBundle):
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin:
        db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin:
        db.add(fin)
    db.prepare()
    assert os.path.exists(f'{ctx.path_working}/wordlist.json')

@ctx
def test_list_transcription_files(db: DataBundle):
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin: db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin: db.add(fin)
    assert set(['1_1_1.eaf', '1_1_1.wav'],) == set(db.list_files())


