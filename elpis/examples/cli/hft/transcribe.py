"""
Example code for transcribing from Python with existing Elpis/HFT model
"""

import argparse
import os
from pathlib import Path
from elpis.engines.common.objects.interface import Interface


def main(model_name, infer_path):

    # Step 0
    # ======
    # Use the Elpis interface directory where all the associated files/objects are stored.
    print('Create interface')
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

    if os.path.isdir('/state/transcriptions/latest'):
        os.remove('/state/transcriptions/latest')
    os.symlink(f'/state/transcriptions/{transcription.hash}',
               '/state/transcriptions/latest',
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
