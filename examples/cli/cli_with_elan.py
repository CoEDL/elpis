# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the
# interface directory already ('dsy', 'mx', 'tx'), if they do, make the kaldi
# interface in a new location.

from elpis.engines.common.objects.interface import Interface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
kaldi = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Setup a dataset to to train data on.
ds = kaldi.new_dataset('dsy')
ds.add_directory('/recordings/transcribed', extensions=['eaf', 'wav'])
ds.auto_select_importer()
# ds.import_with('Elan').import_directory('/recordings/transcribed')
ds.importer.set_setting('tier_name', 'Phrase')

# # Change an importing setting
# ds.importer().change_tier('Phrase')


ds.process()

# Step 2
# ======
# Select Engine
from elpis.engines import ENGINES
engine_name = 'kaldi'
engine = ENGINES[engine_name]
kaldi.set_engine(engine)

# Step 3
# ======
# Build pronunciation dictionary
pd = kaldi.new_pron_dict('pd')
pd.link(ds)
pd.set_l2s_path('/recordings/letter_to_sound.txt')
pd.generate_lexicon()

# Step 4
# ======
# Link dataset and pd to a new model, then train the model.
m = kaldi.new_model('mx')
m.link(ds, pd)
m.build_kaldi_structure()
m.train() # may take a while

# Step 5
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.new_transcription('tx')
t.link(m)
with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
t.transcribe()
print(t.text())
