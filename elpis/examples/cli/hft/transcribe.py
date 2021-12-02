from elpis.engines.common.objects.interface import Interface
from pathlib import Path
import os

MODEL_NAME = 'mx9'
TX_NAME = 'tx'
INFER_FILE_PATH = '/datasets/decode/gk-441.wav'

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
print("Get interface")
elpis = Interface(path='/state', use_existing=True)

# Step 1
# ======
# Select Engine
print('Set engine')
from elpis.engines import ENGINES
engine = ENGINES['hftransformers']
elpis.set_engine(engine)

# Step 2
# ======
# Load Model
print("Get elpis model")
model = elpis.get_model(MODEL_NAME)

# Step 3
# ======
# Make a transcription interface and transcribe audio.

i = 0
tx_name = f"{TX_NAME}{i}"
while tx_name in elpis.list_transcriptions():
    i = i + 1
    tx_name = f"{TX_NAME}{i}"
print('Making new transcriber', tx_name)
transcription = elpis.new_transcription(tx_name)
print('Made transcriber', transcription.hash)

print('Linking model')
transcription.link(model)

if os.path.isdir("/state/transcriptions/latest"):
    os.remove("/state/transcriptions/latest")
os.symlink(f"/state/transcriptions/{transcription.hash}", "/state/transcriptions/latest", target_is_directory=True)


print('Load audio', INFER_FILE_PATH)
with open(INFER_FILE_PATH, 'rb') as faudio:
    transcription.prepare_audio(faudio)

print('Transcribe')
transcription.transcribe()
print(transcription.text())
