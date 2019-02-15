import pytest
import os
import shutil
import hashlib
from .. import paths
from .errors import KaldiError
from .model import Model
from .databundle import DataBundle
from .test_util import Context

ctx = Context(Model, 'model', exclude='data')
ctx.path_working = paths.CURRENT_MODEL_DIR
ctx.path_save = paths.MODELS_DIR
ctx.path_kaldi = paths.kaldi_helpers.INPUT_PATH

##############################################################################
#                           Let the testing begin!                           #
##############################################################################

@ctx
def test__get_status_no_dir(model):
    # remove model dir
    if os.path.exists(ctx.path_working):
        shutil.rmtree(ctx.path_working)
    assert model.get_status(ctx.path_working) == 'No Model'

@ctx
def test__get_status_empty_dir(model):
    assert model.get_status(ctx.path_working) == 'No Model'

@ctx
def test__get_status_after_new_model(model):
    ctx.touch(f'{ctx.path_working}/name.txt')
    ctx.touch(f'{ctx.path_working}/date.txt')
    ctx.touch(f'{ctx.path_working}/hash.txt')
    assert model.get_status(ctx.path_working) == 'Incomplete Model'

@ctx
def test__get_status_after_add_data(model):
    ctx.touch(f'{ctx.path_working}/name.txt')
    ctx.touch(f'{ctx.path_working}/date.txt')
    ctx.touch(f'{ctx.path_working}/hash.txt')
    os.mkdir(f'{ctx.path_working}/data')
    ctx.touch(f'{ctx.path_working}/data/f1.eaf')
    ctx.touch(f'{ctx.path_working}/data/f1.wav')
    ctx.touch(f'{ctx.path_working}/data/f2.eaf')
    ctx.touch(f'{ctx.path_working}/data/f2.wav')
    assert model.get_status(ctx.path_working) == 'Incomplete Model'

@ctx
def test__get_status_after_load_pron_dict(model):
    ctx.touch(f'{ctx.path_working}/name.txt')
    ctx.touch(f'{ctx.path_working}/date.txt')
    ctx.touch(f'{ctx.path_working}/hash.txt')
    ctx.touch(f'{ctx.path_working}/wordlist.json')
    os.mkdir(f'{ctx.path_working}/data')
    ctx.touch(f'{ctx.path_working}/data/f1.eaf')
    ctx.touch(f'{ctx.path_working}/data/f1.wav')
    ctx.touch(f'{ctx.path_working}/data/f2.eaf')
    ctx.touch(f'{ctx.path_working}/data/f2.wav')
    os.mkdir(f'{ctx.path_working}/config')
    ctx.touch(f'{ctx.path_working}/config/letter_to_sound.txt')
    ctx.touch(f'{ctx.path_working}/config/optional_silence.txt')
    ctx.touch(f'{ctx.path_working}/config/silence_phones.txt')
    assert model.get_status(ctx.path_working) == 'Untrained Model'

@ctx
def test__get_status_after_load_pron_dict_and_get_word_list(model):
    # TODO same as test__get_status_after_load_pron_dict but with the word list tiles as well -> 'Untrained Model'
    pass

@ctx
def test_load_pronunciation_dictionary(model):
    pass

@ctx
def test_attaching_empty_data_bundle(model):
    db = DataBundle('db', f'{ctx.path_working}/data', ctx.path_save, ctx.path_kaldi)
    db.new('test db')
    model.new('test model')
    with pytest.raises(KaldiError) as error:
        model.set_data_bundle('test db')
    assert f'data bundle \'test db\' has no data files' == str(error.value)

@ctx
def test_attaching_data_bundle(model):
    # setup data bundle
    path_toy = os.path.join(paths.ELPIS_ROOT_DIR, 'abui_toy_corpus', 'data')
    db = DataBundle('db', f'{ctx.path_working}/data', ctx.path_save, ctx.path_kaldi)
    db.new('test db')
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin: db.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin: db.add(fin)

    # create and add data bundle to model
    model.new('test model ')
    model.set_data_bundle('test db')

    assert os.path.exists(f'{ctx.path_kaldi}/data')
    assert not os.path.exists(f'{ctx.path_working}/data')
    assert os.path.exists(f'{ctx.path_working}/data_bundle_hash.txt')
    
