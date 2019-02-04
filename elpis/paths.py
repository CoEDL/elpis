import os

ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")
MODELS_DIR = os.path.join(ELPIS_ROOT_DIR, 'models')
TRANSCRIPTIONS_DIR = os.path.join(ELPIS_ROOT_DIR, 'transcriptions')
CURRENT_MODELS_DIR = os.path.join(ELPIS_ROOT_DIR, 'current_model')
CURRENT_TRANSCRIPTIONS_DIR = os.path.join(ELPIS_ROOT_DIR, 'current_transcription')


for directory in [
    MODELS_DIR,
    TRANSCRIPTIONS_DIR,
    CURRENT_MODELS_DIR,
    CURRENT_TRANSCRIPTIONS_DIR
]:
    if not os.path.exists(directory):
        os.mkdir(directory)