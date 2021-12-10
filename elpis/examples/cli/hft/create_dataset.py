"""
Use this file to prepare an Elpis dataset from a directory of files on the machine
"""

import argparse
import os
import shutil
from pathlib import Path
from elpis.engines.common.objects.interface import Interface


def main(dataset_name: str, reset: bool):
    presets = {
        'abui': {
            'dataset_dir': '/datasets/abui/transcribed',
            'importer_method': 'tier_name',
            'importer_value': 'Phrase',
        },
        'gk': {
            'dataset_dir': '/datasets/gk',
            'importer_method': 'tier_type',
            'importer_value': 'tx',
        },
        'timit': {
            'dataset_dir': '/datasets/timit/training_data',
            'importer_method': 'tier_name',
            'importer_value': 'default',
        }
    }
    print(f'Using preset for {dataset_name}')
    print(presets[dataset_name])

    # Step 0
    # ======
    # Use or create the Elpis interface directory where all the associated files/objects are stored.
    print('Create interface')
    elpis = Interface(path=Path('/state/of_origin'), use_existing=reset)

    # Step 1
    # ======
    # Select Engine
    print('Set engine')
    from elpis.engines import ENGINES
    elpis.set_engine(ENGINES['hft'])

    # Step 2
    # ======
    # Setup a dataset to to train data on.
    # Reuse dataset if it exists
    print('Current datasets', elpis.list_datasets())
    if dataset_name not in elpis.list_datasets():
        print('Making new dataset', dataset_name)
        dataset = elpis.new_dataset(dataset_name)
        print('Adding data from', presets[dataset_name]['dataset_dir'])
        dataset.add_directory(presets[dataset_name]['dataset_dir'], extensions=['eaf', 'wav'])
        print('Select importer')
        dataset.auto_select_importer() # Selects Elan because of eaf file.
        print('Set setting')
        dataset.importer.set_setting(presets[dataset_name]['importer_method'], presets[dataset_name]['importer_value'])
        print('Process data')
        dataset.process()
    else:
        print('Use existing dataset', dataset_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare a dataset.')
    parser.add_argument('--name',
                        default='abui',
                        type=str,
                        help='Which dataset to use?')
    parser.add_argument('--reset',
                        action='store_false',
                        help='Reset state to create a new dataset with the given name.')
    args = parser.parse_args()

    main(dataset_name=args.name, reset=bool(args.reset))
