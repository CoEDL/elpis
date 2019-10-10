import pytest

from elpis.wrappers.objects.interface import KaldiInterface

@pytest.fixture(scope="session")
def pipeline():
    pass

def test_model_training(tmpdir):
    """
    Test training the model
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pron_dict_y')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()

    m = kaldi.new_model('model_z')
    m.link(ds, pd)
    assert m.has_been_trained() == False
    m.train()
    assert m.has_been_trained == True

    items_in_models_dir = {n for n in m.path.iterdir()}
    assert items_in_models_dir == {'kaldi', 'output', 'text_corpus'}


def test_train_with_unprocessed_dataset():
    pass

def test_train_without_lexicon():
    pass
# TODO: Determine how to achieve further testing without wasting time (training takes a while).