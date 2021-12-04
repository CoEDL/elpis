"""
Use this file to prepare an Elpis dataset from a directory of files on the machine
"""

from elpis.engines.common.objects.interface import Interface
from pathlib import Path
import os


USE_DATASET = 'timit'

if USE_DATASET == 'timit':
    DATASET_DIR = '/datasets/timit/training_data'
    DATASET_NAME = 'timit'
    IMPORTER_METHOD = 'tier_name'
    IMPORTER_VALUE = 'default'
    MODEL_NAME = 'mx'

elif USE_DATASET == 'abui':
    DATASET_DIR = '/datasets/abui/transcribed'
    DATASET_NAME = 'abui'
    IMPORTER_METHOD = 'tier_name'
    IMPORTER_VALUE = 'Phrase'
    MODEL_NAME = 'abui-mx'

else:
    print('which dataset?')
    quit()

# Step 0
# ======
# Create a Kaldi interface directory (where all the associated files/objects will be stored).
elpis = Interface(path=Path('/state'), use_existing=True)


# Step 1
# ======
# Select Engine
print('Set engine')
from elpis.engines import ENGINES
engine = ENGINES['hft']
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
