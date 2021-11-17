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

python elpis/examples/cli/hft/train.py
"""

from elpis.engines.common.objects.interface import Interface
from pathlib import Path


DATASET_DIR = '/datasets/abui/transcribed'
DATASET_NAME = 'ds'
IMPORTER_METHOD = 'tier_name'
IMPORTER_VALUE = 'Phrase'
MODEL_NAME = 'mx'


# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects will be stored).
elpis = Interface(path=Path('/state'), use_existing=True)


# Step 1
# ======
# Select Engine
from elpis.engines import ENGINES
engine = ENGINES['hftransformers']
elpis.set_engine(engine)


# Step 2
# ======
# Setup a dataset to to train data on.
# Reuse dataset if it exists
if DATASET_NAME not in elpis.list_datasets():
    ds = elpis.new_dataset(DATASET_NAME)
    ds.add_directory(DATASET_DIR, extensions=['eaf', 'wav'])
    ds.auto_select_importer() # Selects Elan because of eaf file.
    ds.importer.set_setting(IMPORTER_METHOD, IMPORTER_VALUE)
    ds.process()
else:
    ds = elpis.get_dataset(DATASET_NAME)


# Step 3
# ======
# Link dataset to a new model, then train the model.
i = 0
while MODEL_NAME in elpis.list_models():
    MODEL_NAME = MODEL_NAME + str(i)
print('Making new model', MODEL_NAME)
m = elpis.new_model(MODEL_NAME)
print('Made model', m.hash)
print('Linking dataset')
m.link_dataset(ds)
print('Start training. This may take a while')
m.train()

# TODO infer