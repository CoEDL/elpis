import pytest

from elpis.engines.kaldi.objects.interface import KaldiInterface

# TODO: this file is broken, solution is to fix it or create mock objects

@pytest.fixture(scope="session")
def pipeline_upto_step_0(tmpdir_factory):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 0.
    """

    base_path = tmpdir_factory.mktemp("pipeline")

    # Step 0
    # ======
    # Create a Kaldi interface directory (where all the associated files/objects
    # will be stored).
    kaldi = KaldiInterface(f'{base_path}/state')

    return (kaldi,)


@pytest.fixture(scope="session")
def pipeline_upto_step_1(pipeline_upto_step_0):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 1.
    """

    kaldi, = pipeline_upto_step_0

    # Step 1
    # ======
    # Setup a dataset to to train data on.
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    ds.process()

    return (kaldi, ds)


@pytest.fixture(scope="session")
def pipeline_upto_step_2(pipeline_upto_step_1):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 2.
    """

    kaldi, ds = pipeline_upto_step_1

    # Step 2
    # ======
    # Build pronunciation dictionary
    pd = kaldi.new_pron_dict('pron_dict_y')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()

    return (kaldi, ds, pd)


@pytest.fixture(scope="session")
def pipeline_upto_step_3(pipeline_upto_step_2):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 3.
    """

    kaldi, ds, pd = pipeline_upto_step_2

    # Step 3
    # ======
    # Link dataset and pd to a new model, then train the model.
    m = kaldi.new_model('model_z')
    m.link(ds, pd)
    m.build_kaldi_structure() # TODO: remove this line
    m.train() # may take a while

    return (kaldi, ds, pd, m)


@pytest.fixture(scope="session")
def pipeline_upto_step_4(pipeline_upto_step_3):
    """
    PyTest Fixture: returns a pipeline that executes once per session up to step 4.
    """

    kaldi, ds, pd, m = pipeline_upto_step_3

    # Step 4
    # ======
    # Make a transcription interface and transcribe unseen audio to elan.
    t = kaldi.new_transcription('transcription_w')
    t.link(m)
    t.transcribe_algin('/recordings/untranscribed/audio.wav')

    return (kaldi, ds, pd, m, t)
