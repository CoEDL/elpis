import pytest
import os
import shutil
from .errors import KaldiError
from .interface import KaldiInterface
from .. import paths

def ctx(f):
    interface = KaldiInterface()
    x = interface
    used_paths = [
        x.model._working_path,
        x.model._save_path,
        x.model._kaldi_path,
        x.data_bundle._working_path,
        x.data_bundle._save_path,
        x.data_bundle._kaldi_path,
    ]
    def wrapper():
        for path in used_paths:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)
        f(interface)
        for path in used_paths:
            if os.path.exists(path):
                shutil.rmtree(path)
    return wrapper

@ctx
def test_attaching_empty_data_bundle(kaldi: KaldiInterface):
    kaldi.data_bundle.new('test db')
    kaldi.model.new('test model')
    with pytest.raises(KaldiError) as error:
        kaldi.model.set_data_bundle('test db')
    assert f'data bundle \'test db\' has no data files' == str(error.value)

@ctx
def test_attaching_data_bundle(kaldi: KaldiInterface):
    # setup data bundle
    path_toy = os.path.join(paths.ELPIS_ROOT_DIR, 'abui_toy_corpus', 'data')
    kaldi.data_bundle.new('test db')
    with open(f'{path_toy}/1_1_1.eaf', 'rb') as fin: kaldi.data_bundle.add(fin)
    with open(f'{path_toy}/1_1_1.wav', 'rb') as fin: kaldi.data_bundle.add(fin)

    # create and add data bundle to model
    kaldi.model.new('test model ')
    kaldi.model.set_data_bundle('test db')

    assert os.path.exists(f'{kaldi.model._kaldi_path}/data')
    assert not os.path.exists(f'{kaldi.model._working_path}/data')
    assert os.path.exists(f'{kaldi.model._working_path}/data_bundle_hash.txt')