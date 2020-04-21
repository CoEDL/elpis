import os


# Used by test scripts to tap into a folder of test files
TEST_FILES_BASE_DIR = os.path.join(".", "test", "testfiles")
DEFAULT_DATA_DIRECTORY = os.path.join(".", "resources", "corpora", "abui_toy_corpus", "data")

# Used by resample_audio.py
AUDIO_EXTENSIONS = ["*.wav"]
TEMPORARY_DIRECTORY = "tmp"
SOX_PATH = os.path.join("/", "usr", "bin", "sox")
