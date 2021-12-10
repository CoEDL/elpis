from elpis.engines.common.objects.interface import Interface

MODEL_NAME = 'mx'
TX_NAME = 'tx'
INFER_FILE_PATH = '/datasets/abui/untranscribed/audio.wav'

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path='/state/of_origin', use_existing=True)

# Step 1
# ======
# Select Engine
from elpis.engines import ENGINES
engine = ENGINES['kaldi']
elpis.set_engine(engine)

# Step 2
# ======
# Load Model
m = elpis.get_model(MODEL_NAME)

# Step 3
# ======
# Make a transcription interface and transcribe unseen audio to elan.
t = elpis.new_transcription(TX_NAME)
t.link(m)
with open(INFER_FILE_PATH, 'rb') as faudio:
    t.prepare_audio(faudio)
t.transcribe()
print(t.text())
