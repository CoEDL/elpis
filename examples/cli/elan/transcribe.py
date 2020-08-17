from elpis.engines.common.objects.interface import Interface

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Select Engine
from elpis.engines import ENGINES
engine_name = 'kaldi'
engine = ENGINES[engine_name]
elpis.set_engine(engine)

# Step 2
# ======
# Load Model
m = elpis.get_model('mx')

# Step 3
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = elpis.new_transcription('tx')
t.link(m)
with open('/recordings/untranscribed/audio.wav', 'rb') as faudio:
    t.prepare_audio(faudio)
t.transcribe()
print(t.text())
