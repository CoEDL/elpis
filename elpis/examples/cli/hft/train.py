"""
Example code for using Elpis/HFT from Python
"""

import argparse
import os
from pathlib import Path
from elpis.engines.common.objects.interface import Interface


def main(dataset_name: str, reset: bool):
    presets = {
        'abui': {
            'dataset_dir': '/datasets/abui/transcribed',
            'importer_method': 'tier_name',
            'importer_value': 'Phrase',
            'model_name': 'abui'
        },
        'timit': {
            'dataset_dir': '/datasets/timit/training_data',
            'importer_method': 'tier_name',
            'importer_value': 'default',
            'model_name': 'timit'
        }
    }
    print(f'Using preset for {dataset_name}')
    print(presets[dataset_name])

    # Step 0
    # ======
    # Use or create the Elpis interface directory where all the associated files/objects are stored.
    print('Create interface')
    elpis = Interface(path=Path('/state'), use_existing=reset)

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
        dataset = elpis.get_dataset(dataset_name)

    # Step 3
    # ======
    # Link dataset to a new model, then train the model.
    i = 0
    model_name = f'{presets[dataset_name]["model_name"]}{i}'
    while model_name in elpis.list_models():
        i = i + 1
        model_name = f'{presets[dataset_name]["model_name"]}{i}'
    print('Making new model', model_name)
    model = elpis.new_model(model_name)
    print('Made model', model.hash)
    # TODO add model settings
    print('Linking dataset')
    model.link_dataset(dataset)
    if Path('/state/models/latest').is_dir():
        os.remove('/state/models/latest')
    os.symlink(f'/state/models/{model.hash}', '/state/models/latest', target_is_directory=True)
    print('Start training. This may take a while')
    model.train()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare a dataset and train a model.')
    parser.add_argument('--name',
                        default='abui',
                        type=str,
                        help='Which dataset to use?')
    parser.add_argument('--reset',
                        action='store_false',
                        help='Reset state to create a new dataset and model.')
    args = parser.parse_args()

    main(dataset_name=args.name, reset=bool(args.reset))
