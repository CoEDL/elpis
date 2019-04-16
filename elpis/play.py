# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the
# interface directory already ('dsy', 'mx', 'tx'), if they do, make the kaldi
# interface in a new location.

from kaldi.interface import KaldiInterface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
kaldi = KaldiInterface.load('/elpis/state')

# Step 1
# ======
# Setup a dataset to to train data on.
ds = kaldi.get_dataset('dsy')
with open('/elpis/abui_toy_corpus/data/1_1_4.eaf', 'rb') as feaf, open('/elpis/abui_toy_corpus/data/1_1_4.wav', 'rb') as fwav:
    ds.add_fp(feaf, 'f.eaf')
    ds.add_fp(fwav, 'f.wav')
ds.process()

# Step 2
# ======
# Link dataset to a new model, then train the model.
m = kaldi.get_model('mx')
m.link(ds)
m.set_l2s_path('/elpis/abui_toy_corpus/config/letter_to_sound.txt')
m.generate_lexicon()
m.train() # may take a while

# Step 3
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.get_transcription('tx')
t.link(m)
t.transcribe_align('/elpis/abui_toy_corpus/data/1_1_1.wav')
print(t.elan().decode('utf-8'))
