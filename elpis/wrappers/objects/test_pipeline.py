import pytest

from elpis.wrappers.objects.interface import KaldiInterface

@pytest.fixture(scope="session")
def pipeline(tmpdir_factory):
    """
    PyTest Fixture: returns a pipeline that executes once per session.
    """
    
    base_path = tmpdir_factory.mktemp("pipeline")

    # Step 0
    # ======
    # Create a Kaldi interface directory (where all the associated files/objects
    # will be stored).
    kaldi = KaldiInterface(f'{base_path}/state')

    # Step 1
    # ======
    # Setup a dataset to to train data on.
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')

    # Step 2
    # ======
    # Build pronunciation dictionary
    pd = kaldi.new_pron_dict('pron_dict_y')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()

    # Step 3
    # ======
    # Link dataset and pd to a new model, then train the model.
    m = kaldi.new_model('model_z')
    m.link(ds, pd)
    m.build_kaldi_structure() # TODO: remove this line
    m.train() # may take a while


    # Step 4
    # ======
    # Make a transcription interface and transcribe unseen audio to elan.
    t = kaldi.new_transcription('transcription_w')
    t.link(m)
    t.transcribe_algin('/recordings/untranscribed/audio.wav')

    return (kaldi, ds, pd, m, t)