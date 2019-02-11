import hashlib
import json
import os
import time
import shutil
from typing import List, Tuple

from . import step, KaldiError, task
from .. import paths

# When synchronizing between the local model (current_model/) and the kaldi
# location (/kaldi-helpers/working_dir/input), be sure to use the correct
# sync_to_* function. Functions that make changes should only do so in either
# the local location or the kaldi location but not both. That way changes can
# be guarantee to carry to the other location cleanly. If modifications are
# made in the local location, then use _sync_to_kaldi, and vise versa.
def _sync_to_kaldi():
    """Copy files from local model to kaldi helpers"""
    if os.path.exists(paths.kaldi_helpers.INPUT_PATH):
        shutil.rmtree(paths.kaldi_helpers.INPUT_PATH)
    shutil.copytree(paths.CURRENT_MODEL_DIR, paths.kaldi_helpers.INPUT_PATH)

def _sync_to_local():
    """Copy files from kaldi helpers to local model"""
    if os.path.exists(paths.CURRENT_MODEL_DIR):
        shutil.rmtree(paths.CURRENT_MODEL_DIR)
    shutil.copytree(paths.kaldi_helpers.INPUT_PATH, paths.CURRENT_MODEL_DIR)
    pass

def get_list() -> List[str]:
    """Returns the list of model names that have been saved. Models are saved
    in the paths.MODELS_DIR directory.
    """
    names = []
    for model_dir in os.listdir(paths.MODELS_DIR):
        with open(f'{paths.MODELS_DIR}/{model_dir}/name.txt', 'r') as fin:
            names.append(fin.read())
    return names

def _get_status(directory) -> str:
    def no_model() -> bool:
        return not os.path.exists(directory) or (
            len(os.listdir(directory)) == 0
        )
    def complete_model() -> bool:
        return sorted(os.listdir(directory)) == sorted([
                'data',
                'config',
                'name.txt',
                'date.txt',
                'hash.txt',
                'wordlist.json',
            ]) and (
                len(os.listdir(f'{directory}/data')) != 0 and sorted([
                    'letter_to_sound.txt',
                    'optional_silence.txt',
                    'silence_phones.txt'
                ]) == sorted(os.listdir(f'{directory}/config'))
            )
    if no_model(): return 'No Model'
    elif not complete_model(): return 'Incomplete Model'
    else: return 'Untrained Model'

def get_status():
    # TODO: unimplemented
    return None

def get_info_of(name):
    # TODO: unimplemented
    return {}

def _check_name(name):
    if name in get_list():
        raise KaldiError(f'model already exists with the name: \'{name}\'')
    if name == '':
        raise KaldiError('invalid model name: \'\'')

@step()
def new(name):
    """
    Clears the current model and creates a new model.

    Before running this command, the current_model/ directory could be in any
    state. On running this command, the contents is deleted so that a new 
    model can take its place.

    The filesystem state after running this command is:
    current_model/
        name.txt
        date.txt
        hash.txt
    
    :raise KaldiError: if there is an attempts to create a model that already
    exists or if the name is invalid.
    """
    _check_name(name)
    if os.path.exists(paths.CURRENT_MODEL_DIR):
        shutil.rmtree(paths.CURRENT_MODEL_DIR)
    os.mkdir(paths.CURRENT_MODEL_DIR)
    # write state files
    date = time.time()
    with open(f'{paths.CURRENT_MODEL_DIR}/name.txt', 'w') as fout:
        fout.write(name)
    with open(f'{paths.CURRENT_MODEL_DIR}/date.txt', 'w') as fout:
        fout.write(str(date))
    with open(f'{paths.CURRENT_MODEL_DIR}/hash.txt', 'w') as fout:
        hashname = hashlib.md5(bytes(str(date), 'utf-8')).hexdigest()
        fout.write(hashname)
    _sync_to_kaldi()

def get_name() -> str:
    if os.path.exists(f'{paths.CURRENT_MODEL_DIR}/name.txt'):
        with open(f'{paths.CURRENT_MODEL_DIR}/name.txt', 'r') as fin:
            return fin.read()
    return None

def change_name(name):
    if os.path.exists(f'{paths.CURRENT_MODEL_DIR}/name.txt'):
        _check_name(name)
        with open(f'{paths.CURRENT_MODEL_DIR}/name.txt', 'w') as fout:
            fout.write(name)
        # Below I am breaking the rule about only making changes to one
        # location, then running a sync function, however, syncing may take
        # too long if we are updating the name everytime the user types. So
        # just here I break the rule ;)
        with open(f'{paths.kaldi_helpers.INPUT_PATH}/name.txt', 'w') as fout:
            fout.write(name)
    else:
        raise KaldiError('Need to create a model before changing the name')


def get_date() -> float:
    if os.path.exists(f'{paths.CURRENT_MODEL_DIR}/date.txt'):
        with open(f'{paths.CURRENT_MODEL_DIR}/date.txt', 'r') as fin:
            return float(fin.read())
    return None

def get_hash() -> str:
    if os.path.exists(f'{paths.CURRENT_MODEL_DIR}/hash.txt'):
        with open(f'{paths.CURRENT_MODEL_DIR}/hash.txt', 'r') as fin:
            return fin.read()
    return None

File = Tuple[str, str]
FilePair = Tuple[File, File]

@step(deps=[new])
def load_transcription_files(file_pairs: List[FilePair]):
    """
    :param file_pairs: is a list of paired tuples of tuples... file_pairs is
    a list of (FILE, FILE), while FILE is a tuple representing a file by
    (filename, filecontent).
    """
    if not os.path.exists(f'{paths.CURRENT_MODEL_DIR}/data'):
        os.mkdir(f'{paths.CURRENT_MODEL_DIR}/data')
    for pair in file_pairs:
        for filename, filecontent in pair:
            with open(f'{paths.CURRENT_MODEL_DIR}/data/{filename}', 'wb') as fout:
                fout.write(filecontent)
    _sync_to_kaldi()

def get_transcription_files() -> List[str]:
    return [ name for name in os.listdir(f'{paths.CURRENT_MODEL_DIR}/data')]

@step(deps=[load_transcription_files])
def generate_word_list():
    # only steps 1 and 2 of _run-elan
    p = task('clean-output-folder tmp-makedir make-kaldi-subfolders')
    p = task('elan-to-json')
    _sync_to_local()
    wordlist = {}
    path = f'{paths.kaldi_helpers.INPUT_PATH}/output/tmp/dirty.json'
    with open(path, 'r') as fin:
        dirty = json.load(fin)
    for transcription in dirty:
        words = transcription['transcript'].split()
        for word in words:
            if word in wordlist:
                wordlist[word] += 1
            else:
                wordlist[word] = 1
    with open(f'{paths.CURRENT_MODEL_DIR}/wordlist.json', 'w') as fout:
        json.dump(wordlist, fout)
    _sync_to_kaldi()

def get_wordlist() -> str:
    if os.path.exists(f'{paths.CURRENT_MODEL_DIR}/wordlist.json'):
    with open(f'{paths.CURRENT_MODEL_DIR}/wordlist.json', 'r') as fin:
        return fin.read()
    return None

@step(deps=[generate_word_list])
def load_pronunciation_dictionary(filecontent):
    # TODO: unimplemented
    return ''

def get_pronunciation_dictionary():
    """
    :return: None if the pronunciation dictionary has yet to be loaded,
    otherwise, the content of the pronunciation dictionary is returned
    """
    # TODO: unimplemented
    return None

@step(deps=[new])
def load_settings(file):
    # TODO: unimplemented
    return ''

def get_settings():
    # TODO: unimplemented
    return None

@step(deps=[load_settings, generate_word_list, load_pronunciation_dictionary])
def train():
    # TODO: unimplemented
    return ''

def load(name):
    # TODO: unimplemented
    return None

def save():
    # TODO: unimplemented
    return None

def get_training_results():
    # TODO: unimplemented
    return None