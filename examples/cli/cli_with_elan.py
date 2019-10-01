# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the
# interface directory already ('dsy', 'mx', 'tx'), if they do, make the kaldi
# interface in a new location.

from elpis.wrappers.objects.interface import KaldiInterface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
kaldi = KaldiInterface('/workspaces/elpis/state', use_existing=True)

# Step 1
# ======
# Setup a dataset to to train data on.
ds = kaldi.new_dataset('dsy', override=True)
# ds.add_directory('/recordings/transcribed', filter=['eaf', 'wav'])
elan = ds.import_with('Elan')
elan.import_directory('/recordings/transcribed')
elan.
ds.process()

# Step 2
# ======
# Build pronunciation dictionary
pd = kaldi.new_pron_dict('pd', override=True)
pd.link(ds)
pd.set_l2s_path('/recordings/letter_to_sound.txt')
pd.generate_lexicon()

# Step 3
# ======
# Link dataset and pd to a new model, then train the model.
m = kaldi.new_model('mx', override=True)
m.link(ds, pd)
m.build_kaldi_structure()
m.train() # may take a while

# Step 4
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.new_transcription('tx', override=True)
t.link(m)
with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
# t.transcribe_align()
t.transcribe()
# print(t.elan().decode('utf-8'))
print(t.text().decode('utf-8'))
