import os


ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")
USER_DATA = os.path.join(ELPIS_ROOT_DIR, 'user_data')
DATABUNDLES_DIR = os.path.join(USER_DATA, 'databundles')
MODELS_DIR = os.path.join(USER_DATA, 'models')
TRANSCRIPTIONS_DIR = os.path.join(USER_DATA, 'transcriptions')
CURRENT_DATABUNDLE_DIR = os.path.join(USER_DATA, 'databundles')
CURRENT_MODEL_DIR = os.path.join(USER_DATA, 'current_model')
CURRENT_TRANSCRIPTION_DIR = os.path.join(USER_DATA, 'current_transcription')


