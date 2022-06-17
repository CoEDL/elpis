import pytest

from elpis.wrappers.objects.interface import KaldiInterface


@pytest.fixture
def pipeline_upto_step_1(tmpdir):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 1.
    """

    # Step 0
    # ======
    # Create a Kaldi interface directory (where all the associated files/objects
    # will be stored).
    kaldi = KaldiInterface(f"{tmpdir}/state")

    # Step 1
    # ======
    # Setup a dataset to to train data on.
    ds = kaldi.new_dataset("dataset_x")
    ds.add_directory("/recordings/transcribed")
    ds.select_importer("Elan")
    ds.process()

    return (kaldi, ds)


def test_model_training(pipeline_upto_step_1):
    """
    Test training the model
    """
    kaldi, ds = pipeline_upto_step_1
    pd = kaldi.new_pron_dict("pron_dict_y")
    pd.link(ds)
    pd.set_l2s_path("/recordings/letter_to_sound.txt")
    pd.generate_lexicon()

    m = kaldi.new_model("model_z")
    m.link(ds, pd)
    assert m.has_been_trained() == False
    m.build_structure()
    m.train()
    assert m.has_been_trained() == True
    return


# TODO: Determine how to achieve further testing without wasting time (training takes a while).
