"""
Example code for using Elpis/Kaldi from Python

Start Elpis Docker container, share a volume containing your dataset, e.g.:

docker run --rm -it -p 5001:5001/tcp \
  -v ~/sandbox/datasets:/datasets \
  -v ~/sandbox/state:/state \
  -v ~/sandbox/elpis:/elpis \
  --entrypoint /bin/zsh \
  coedl/elpis:latest

Change dataset dir values etc below to suit your data.
Run the data preparation scripts and do training by calling this script from the /elpis dir.

poetry shell
python elpis/examples/cli/kaldi/train.py
"""

from elpis.engines.common.objects.interface import Interface
from pathlib import Path
from loguru import logger

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
    logger.info("Making new dataset")
    dataset = elpis.new_dataset(DATASET_NAME)
    dataset.add_directory(DATASET_DIR, extensions=['eaf', 'wav'])
    dataset.auto_select_importer() # Selects Elan because of eaf file.
    dataset.importer.set_setting(IMPORTER_METHOD, IMPORTER_VALUE)
    dataset.process()
else:
    logger.info("Use existing dataset")
    dataset = elpis.get_dataset(DATASET_NAME)


# Step 3
# ======
# Build pronunciation dictionary
# Reuse pronunciation dictionary if it exists
if PRON_DICT_NAME not in elpis.list_pron_dicts():
    logger.info("Making new pron dict")
    pron_dict = elpis.new_pron_dict(PRON_DICT_NAME)
    pron_dict.link(dataset)
    pron_dict.set_l2s_path(L2S_PATH)
    pron_dict.generate_lexicon()
else:
    logger.info("Use existing pron dict")
    pron_dict = elpis.get_pron_dict(PRON_DICT_NAME)


# Step 4
# ======
# Link dataset and pd to a new model, then train the model.
# Load model if it exists
if MODEL_NAME not in elpis.list_models():
    logger.info("Making new model")
    model = elpis.new_model(MODEL_NAME)
    model.link_dataset(dataset)
    model.link_pron_dict(pron_dict)
    model.build_structure()
    model.train() # may take a while
else:
    logger.info("Use existing model")
    model = elpis.get_model(MODEL_NAME)
