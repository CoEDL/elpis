from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import soundfile as sf
import librosa

from werkzeug.datastructures import FileStorage


ORIGINAL_SOUND_FILE_DIRECTORY = Path('/tmp/origial_sound_files/')


def load_audio(file: Path, target_sample_rate: int = None) -> Tuple[np.ndarray, int]:
    """Loads a file and returns the data wtihin.

    Parameters:
        file (Path): The path of the file to load.
        target_sample_rate (int): An optional sample rate with which to load the
            audio data.

    Returns:
        (Tuple<np.ndarray, int>): A tuple containing the numpy array of
            the audio data, and the native sample rate of the file.
    """
    return librosa.load(file, sr=target_sample_rate)

def resample_audio(file: Path, destination: Path, target_sample_rate: int) -> None:
    """Writes a resampled audio file to the supplied destination, with a supplied
    sample rate.

    Parameters:
        file (Path): The path of the file to resample
        destination (Path): The destination at which to create the resampled file
        target_sample_rate (int): The target sample rate for the resampled audio.
    """
    data, sample_rate = librosa.load(file)

    # Create temporary directory if it hasn't already been created
    ORIGINAL_SOUND_FILE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    # Copy audio to the temporary path
    original = ORIGINAL_SOUND_FILE_DIRECTORY / file.name
    sf.write(original, data, sample_rate)

    # Resample and overwrite
    sf.write(destination, data, target_sample_rate)


def resample_from_file_storage(file: FileStorage, destination: Path, target_sample_rate: int) -> Dict:
    """ Performs audio resampling from a flask request FileStorage file, and
    returns some information about the original file.
    
    """
    # Create temporary directory if it hasn't already been created
    ORIGINAL_SOUND_FILE_DIRECTORY.mkdir(parents=True, exist_ok=True)

    original = ORIGINAL_SOUND_FILE_DIRECTORY / file.filename
    with original.open(mode='wb') as fout:
        fout.write(file.read())

    info = {
        'duration': librosa.get_duration(filename=original)
    }

    resample_audio(original, destination, target_sample_rate)
    return info