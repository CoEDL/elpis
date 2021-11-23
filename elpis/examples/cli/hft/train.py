"""
Example code for using Elpis/HFT from Python

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
python elpis/examples/cli/hft/train.py
"""

from elpis.engines.common.objects.interface import Interface
from pathlib import Path


DATASET_DIR = '/datasets/gk'
DATASET_NAME = 'gk'
IMPORTER_METHOD = 'tier_type'
IMPORTER_VALUE = 'tx'
MODEL_NAME = 'mx'


# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects will be stored).
elpis = Interface(path=Path('/state'), use_existing=True)


# Step 1
# ======
# Select Engine
print('Set engine')
from elpis.engines import ENGINES
engine = ENGINES['hftransformers']
elpis.set_engine(engine)


# Step 2
# ======
# Setup a dataset to to train data on.
# Reuse dataset if it exists
if DATASET_NAME not in elpis.list_datasets():
    print('Making new dataset', DATASET_NAME)
    dataset = elpis.new_dataset(DATASET_NAME)
    print('Adding data from', DATASET_DIR)
    dataset.add_directory(DATASET_DIR, extensions=['eaf', 'wav'])
    print('Select importer')
    dataset.auto_select_importer() # Selects Elan because of eaf file.
    print('Set setting')
    dataset.importer.set_setting(IMPORTER_METHOD, IMPORTER_VALUE)
    print('Process data')
    dataset.process()
else:
    print('Use existing dataset', DATASET_NAME)
    dataset = elpis.get_dataset(DATASET_NAME)


# Step 3
# ======
# Link dataset to a new model, then train the model.
i = 0
model_name = f"{MODEL_NAME}{i}"
while model_name in elpis.list_models():
    i = i + 1
    model_name = f"{MODEL_NAME}{i}"
print('Making new model', model_name)
model = elpis.new_model(model_name)
print('*** Made model', model.hash)
print('Linking dataset')
model.link_dataset(dataset)
print('Start training. This may take a while')
model.train()

# TODO infer
