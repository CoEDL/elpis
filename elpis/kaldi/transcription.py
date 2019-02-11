from . import step

def get_status():
    # TODO: unimplemented
    return 'No Transcription'

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
def select_model(model_name):
    # TODO: unimplemented
    return None

def get_selected_model():
    # TODO: unimplemented
    return None

@step(deps=[new])
def load_audio(files):
    # TODO: unimplemented
    return None

def get_audio_files():
    return []

@step(deps=[select_model, load_audio])
def transcribe():
    # TODO: unimplemented
    return None

def load(name):
    # TODO: unimplemented
    return None

def save():
    # TODO: unimplemented
    return None

def get_list():
    # TODO: unimplemented
    return None

def get_transcription_results():
    # TODO: unimplemented
    return None
