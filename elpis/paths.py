import os
ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")
MODELS_DIR = os.path.join(ELPIS_ROOT_DIR, 'models')