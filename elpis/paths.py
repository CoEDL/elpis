import os

ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")
MODELS_DIR = os.path.join(ELPIS_ROOT_DIR, 'models')
TRANSCRIPTIONS_DIR = os.path.join(ELPIS_ROOT_DIR, 'transcriptions')
CURRENT_MODEL_DIR = os.path.join(ELPIS_ROOT_DIR, 'current_model')
CURRENT_TRANSCRIPTION_DIR = os.path.join(ELPIS_ROOT_DIR, 'current_transcription')


for directory in [
    MODELS_DIR,
    TRANSCRIPTIONS_DIR,
    CURRENT_MODEL_DIR,
    CURRENT_TRANSCRIPTION_DIR
]:
    if not os.path.exists(directory):
        os.mkdir(directory)

class kaldi_helpers:
    KALDI_ROOT = "/kaldi"
    HELPERS_PATH = "/kaldi-helpers"
    KALDI_TEMPLATES = "/kaldi-helpers/resources/kaldi_templates"
    INPUT_SCRIPTS_PATH = "kaldi_helpers/input_scripts"
    OUTPUT_SCRIPTS_PATH = "kaldi_helpers/output_scripts"
    INFERENCE_SCRIPTS_PATH = "kaldi_helpers/inference_scripts"
    INPUT_PATH = "/kaldi-helpers/working_dir/input"
    KALDI_OUTPUT_PATH = "working_dir/input/output"
    WORKING_OUTPUT_PATH = "working_dir/output"
    CORPUS_PATH = "working_dir/input/data"
    INFER_PATH = "working_dir/input/infer"
    CLEANED_FILTERED_DATA = "cleaned_filtered.json"
    LETTER_TO_SOUND_PATH = "working_dir/input/config/letter_to_sound.txt"
    SILENCE_PHONES_PATH = "working_dir/input/config/silence_phones.txt"
    OPTIONAL_SILENCE_PHONES_PATH = "working_dir/input/config/optional_silence.txt"