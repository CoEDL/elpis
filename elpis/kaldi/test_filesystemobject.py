import pytest
import os
from .errors import KaldiError
from .fsobject import FileSystemObject
from .test_util import Context

ctx = Context(FileSystemObject, 'obj', exclude='data')

@ctx
def test_new(obj):
    obj.new('daffy duck')
    with open(f'{ctx.path_working}/name.txt', 'r') as fin:
        name = fin.read()
    assert name == 'daffy duck'
    assert os.path.exists(f'{ctx.path_working}/date.txt')
    assert os.path.exists(f'{ctx.path_working}/hash.txt')

@ctx
def test_sync_to_kaldi(obj):
    ctx.touch(f'{ctx.path_working}/sync')
    assert not os.path.exists(f'{ctx.path_kaldi}/sync')
    obj.sync_to_kaldi()
    assert os.path.exists(f'{ctx.path_kaldi}/sync')

@ctx
def test_sync_to_working(obj):
    ctx.touch(f'{ctx.path_kaldi}/sync')
    assert not os.path.exists(f'{ctx.path_working}/sync')
    obj.sync_to_working()
    assert os.path.exists(f'{ctx.path_working}/sync')

@ctx
def test_get_list(obj):
    # add stub objs
    os.mkdir(f'{ctx.path_save}/m1')
    with open(f'{ctx.path_save}/m1/name.txt', 'w') as fout:
        fout.write('carlos')
    os.mkdir(f'{ctx.path_save}/m2')
    with open(f'{ctx.path_save}/m2/name.txt', 'w') as fout:
        fout.write('dallis')
    os.mkdir(f'{ctx.path_save}/m3')
    with open(f'{ctx.path_save}/m3/name.txt', 'w') as fout:
        fout.write('other nic')
    # Test the results
    names = obj.get_list()
    assert 'carlos' in names
    assert 'other nic' in names
    assert 'dallis' in names

@ctx
def test_new_obj_already_exists(obj):
    os.mkdir(f'{ctx.path_save}/m')
    with open(f'{ctx.path_save}/m/name.txt', 'w') as fout:
        fout.write('bugs bunny')
    with pytest.raises(KaldiError) as error:
        obj.new('bugs bunny')
    assert 'obj already exists with the name: \'bugs bunny\'' == str(error.value)

@ctx
def test_new_invalid_name(obj):
    with pytest.raises(KaldiError) as error:
        obj.new('')
    assert 'invalid obj name: \'\'' == str(error.value)

@ctx
def test_new_with_sync(obj):
    obj.new('nildocaafiat')
    namefile = f'{ctx.path_kaldi}/name.txt'
    assert os.path.exists(namefile)
    with open(namefile, 'r') as fin:
        assert fin.read() == 'nildocaafiat'

@ctx
def test_get_name(obj):
    obj.new('nildocaafiat')
    assert obj.get_name() == 'nildocaafiat'

@ctx
def test_get_date(obj):
    obj.new('nildocaafiat')
    assert obj.get_date() > 1

@ctx
def test_get_hash(obj):
    obj.new('nildocaafiat')
    allowed_chars = set('abcdefABCDEF0123456789')
    assert set(obj.get_hash()).issubset(allowed_chars)

@ctx
def test_sync_with_exclude(obj):
    os.mkdir(f'{ctx.path_working}/data')
    ctx.touch(f'{ctx.path_working}/data/d1')
    ctx.touch(f'{ctx.path_working}/data/d2')
    ctx.touch(f'{ctx.path_working}/data/d_who')
    ctx.touch(f'{ctx.path_working}/data/d_you')
    ctx.touch(f'{ctx.path_working}/cat')
    ctx.touch(f'{ctx.path_working}/in')
    ctx.touch(f'{ctx.path_working}/a')
    ctx.touch(f'{ctx.path_working}/hat')
    obj.sync_to_kaldi()
    assert not os.path.exists(f'{ctx.path_kaldi}/data')
    assert os.path.exists(f'{ctx.path_kaldi}/cat')