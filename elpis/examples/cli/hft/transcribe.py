"""
Example code for transcribing from Python with existing Elpis/HFT model
"""

import argparse
import os
from pathlib import Path
from elpis.engines.common.objects.interface import Interface


def main(model_name: str, infer_path: str):

    # Step 0
    # ======
    # Use the Elpis interface directory where all the associated files/objects are stored.
    print('Create interface')
    elpis = Interface(path=Path('/state/of_origin'), use_existing=True)

    # Step 1
    # ======
    # Select Engine
    print('Set engine')
    from elpis.engines import ENGINES
    elpis.set_engine(ENGINES['hft'])

    # Step 2
    # ======
    # Load Model
    print(f'Get elpis model for {model_name}')
    model = elpis.get_model(model_name)

    # Step 3
    # ======
    # Make a transcription interface and transcribe audio.
    i = 0
    base_name = 'tx'
    tx_name = f'{base_name}{i}'
    while tx_name in elpis.list_transcriptions():
        i = i + 1
        tx_name = f'{base_name}{i}'
    print('Making new transcriber', tx_name)
    transcription = elpis.new_transcription(tx_name)
    print('Made transcriber', transcription.hash)
    print('Linking model')
    transcription.link(model)

    if Path('/state/of_origin/transcriptions/latest').is_dir():
        os.remove('/state/of_origin/transcriptions/latest')
    os.symlink(f'/state/of_origin/transcriptions/{transcription.hash}',
               '/state/of_origin/transcriptions/latest',
               target_is_directory=True)

    print(f'Load audio from {infer_path}')
    with open(infer_path, 'rb') as infer_audio_file:
        transcription.prepare_audio(infer_audio_file)

    print('Transcribe')
    transcription.transcribe()
    print(transcription.text())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a file.')
    parser.add_argument('--name',
                        default='abui0',
                        type=str,
                        help='Which dataset to use?'
                        )
    parser.add_argument('--infer',
                        default='/datasets/abui/untranscribed/audio.wav',
                        type=str,
                        help='Which file to transcribe?'
                        )
    args = parser.parse_args()

    main(model_name=args.name, infer_path=args.infer)
