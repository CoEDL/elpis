"""
Example code for using Elpis/Kaldi from Python

Start Elpis Docker container, share a volume containing your dataset, e.g.:

docker run --rm -it -p 5000:5000/tcp \
  -v ~/sandbox/datasets:/datasets \
  -v ~/sandbox/state:/state \
  -v ~/sandbox/elpis:/elpis \
  --entrypoint /bin/zsh \
  coedl/elpis:hft

Change dataset dir values etc below to suit your data.
Run the data preparation scripts and do training by calling this script from the /elpis dir.

python elpis/examples/cli/kaldi/train.py
"""

from elpis.engines.common.objects.interface import Interface
from pathlib import Path


DATASET_DIR = '/datasets/abui/transcribed'
DATASET_NAME = 'ds'
IMPORTER_METHOD = 'tier_name'
IMPORTER_VALUE = 'Phrase'
L2S_PATH = '/datasets/abui/letter_to_sound.txt'
PRON_DICT_NAME = 'pd'
MODEL_NAME = 'mx'
TX_NAME = 'tx'
INFER_FILE_PATH = '/datasets/abui/untranscribed/audio.wav'

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects
# will be stored).
elpis = Interface(path=Path('/state'), use_existing=True)


# Step 1
# ======
# Select Engine
from elpis.engines import ENGINES
engine = ENGINES['kaldi']
elpis.set_engine(engine)


# Step 2
# ======
# Setup a dataset to to train data on.
# Reuse dataset if it exists
if DATASET_NAME not in elpis.list_datasets():
    print("Making new dataset")
    ds = elpis.new_dataset(DATASET_NAME)
    ds.add_directory(DATASET_DIR, extensions=['eaf', 'wav'])
    ds.auto_select_importer() # Selects Elan because of eaf file.
    ds.importer.set_setting(IMPORTER_METHOD, IMPORTER_VALUE)
    ds.process()
else:
    print("Use existing dataset")
    ds = elpis.get_dataset(DATASET_NAME)


# Step 3
# ======
# Build pronunciation dictionary
# Reuse pronunciation dictionary if it exists
if PRON_DICT_NAME not in elpis.list_pron_dicts():
    print("Making new pron dict")
    pd = elpis.new_pron_dict(PRON_DICT_NAME)
    pd.link(ds)
    pd.set_l2s_path(L2S_PATH)
    pd.generate_lexicon()
else:
    print("Use existing pron dict")
    pd = elpis.get_pron_dict(PRON_DICT_NAME)


# Step 4
# ======
# Link dataset and pd to a new model, then train the model.
# Load model if it exists
if MODEL_NAME not in elpis.list_models():
    print("Making new model")
    m = elpis.new_model(MODEL_NAME)
    m.link_dataset(ds)
    m.link_pron_dict(pd)
    m.build_structure()
    m.train() # may take a while
else:
    print("Use existing model")
    m = elpis.get_model(MODEL_NAME)


# Step 5
# ======
# Make a transcription interface and transcribe audio.
i = 0
while TX_NAME in elpis.list_transcriptions():
    TX_NAME = TX_NAME + str(i)
t = elpis.new_transcription(TX_NAME)
t.link(m)
with open(INFER_FILE_PATH, 'rb') as faudio:
    t.prepare_audio(faudio)
t.transcribe()
print(t.text())
