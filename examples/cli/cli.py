# Example code for using elpis from python.

# Must run from the docker contianer and the objects must not exist in the
# interface directory already ('dsy', 'mx', 'tx'), if they do, make the kaldi
# interface in a new location.

from elpis.wrappers.objects.interface import KaldiInterface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
kaldi = KaldiInterface('/elpis/state')

# Step 1
# ======
# Setup a dataset to to train data on.
ds = kaldi.new_dataset('dsy')
ds.add_directory('/recordings/transcribed', filter=['eaf', 'wav'])
ds.process()

# Step 2
# ======
# Link dataset to a new model, then train the model.
m = kaldi.new_model('mx')
m.link(ds)
m.set_l2s_path('/recordings/letter_to_sound.txt')
m.generate_lexicon()
m.train() # may take a while

# Step 3
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = kaldi.new_transcription('tx')
t.link(m)
with open('/recordings/untranscribed.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
# t.transcribe_align()
t.transcribe()
# print(t.elan().decode('utf-8'))
print(t.text().decode('utf-8'))
