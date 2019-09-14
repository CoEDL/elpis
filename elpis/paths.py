import os

# Trying to remove the need for this file. Unconfirmed, but all variables
# under USER_DATA are no longer used/supported by the codebase.

ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")

USER_DATA = os.path.join(ELPIS_ROOT_DIR, 'user_data')
DATASETS_DIR = os.path.join(USER_DATA, 'datasets')
PRON_DICTS_DIR = os.path.join(USER_DATA, 'pron_dicts')
MODELS_DIR = os.path.join(USER_DATA, 'models')
TRANSCRIPTIONS_DIR = os.path.join(USER_DATA, 'transcriptions')
CURRENT_DATASET_DIR = os.path.join(USER_DATA, 'datasets')
CURRENT_PRON_DICT_DIR = os.path.join(USER_DATA, 'pron_dicts')
CURRENT_MODEL_DIR = os.path.join(USER_DATA, 'current_model')
CURRENT_TRANSCRIPTION_DIR = os.path.join(USER_DATA, 'current_transcription')


