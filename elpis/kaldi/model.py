from . import step

def get_status():
    # TODO: unimplemented
    return 'No Model'

def get_info_of(name):
    # TODO: unimplemented
    return {}

@step
def new(name):
    # TODO: unimplemented
    return None

def get_name():
    # TODO: unimplemented
    return None

@step(deps=[new])
def load_transcription_files(file_pairs, overwrite=False):
    """
    :param file_pairs: is a list of paired tuples of tuples... file_pairs is
    a list of (FILE, FILE), while FILE is a tuple representing a file by
    (filename, filecontent).
    :param overwrite: if true, and a file already exists, then it'll be
    overwritten, otherwise, it will just be skipped.
    :raise KaldiError: if file names in the pair don't match.
    """
    # TODO: unimplemented
    return None

def get_transcription_files():
    """
    Get a list of files 
    """
    # TODO: unimplemented
    return None

@step(deps=[load_transcription_files])
def generate_word_list():
    # TODO: unimplemented
    return ''

@step(deps=[load_transcription_files])
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

def get_list():
    # TODO: unimplemented
    return None

def get_training_results():
    # TODO: unimplemented
    return None