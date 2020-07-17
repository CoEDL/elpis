# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the
# interface directory already ('dsy', 'mx', 'tx'), if they do, make the kaldi
# interface in a new location.

from elpis.engines.common.objects.interface import Interface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Setup a dataset to to train data on.
if 'dsy' not in elpis.list_datasets():
    ds = elpis.new_dataset('dsy')
    ds.add_directory('/recordings/transcribed', extensions=['eaf', 'wav'])
    ds.auto_select_importer() # Selects Elan because of eaf file.
    ds.importer.set_setting('tier_name', 'Phrase')
    ds.process()
else:
    ds = elpis.get_dataset('dsy')

# Step 2
# ======
# Select Engine
from elpis.engines import ENGINES
engine_name = 'kaldi'
engine = ENGINES[engine_name]
elpis.set_engine(engine)

# Step 3
# ======
# Build pronunciation dictionary
if 'pd' not in elpis.list_pron_dicts():
    pd = elpis.new_pron_dict('pd')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()
else:
    pd = elpis.get_pron_dict('pd')

# Step 4
# ======
# Link dataset and pd to a new model, then train the model.
if 'mx' not in elpis.list_models():
    m = elpis.new_model('mx')
    m.link(ds, pd)
    m.build_kaldi_structure()
    m.train() # may take a while
else:
    m = elpis.get_model('mx')

# Step 5
# ======
# Make a transcription interface and transcribe unseen audio to elan.
if 'tx' not in elpis.list_transcriptions():
    t = elpis.new_transcription('tx')
    t.link(m)
    with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
        t.prepare_audio(faudio)
    t.transcribe()
else:
    t = elpis.get_transcription('tx')
print(t.text())
