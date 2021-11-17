from elpis.engines.common.objects.interface import Interface

MODEL_NAME = 'mx'
TX_NAME = 'tx'
INFER_FILE_PATH = '/datasets/abui/untranscribed/audio.wav'

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Select Engine
from elpis.engines import ENGINES
engine = ENGINES['kaldi']
elpis.set_engine(engine)

# Step 2
# ======
# Load Model
model = elpis.get_model(MODEL_NAME)

# Step 3
# ======
# Make a transcription interface and transcribe audio.
# TODO fix this .. prepare_audio expects a request.file object
# transcription.link(model)
# transcription = elpis.new_transcription(TX_NAME)
# with open(INFER_FILE_PATH, 'rb') as faudio:
#     transcription.prepare_audio(faudio)
# transcription.transcribe()
# print(transcription.text())
