from .model import Model
from .databundle import DataBundle
from .transcription import Transcription
from .. import paths

class KaldiInterface(object):
    def __init__(self):
        super().__init__()
        self.data_bundle = DataBundle(
            self,
            'data bundle',
            paths.CURRENT_DATABUNDLE_DIR,
            paths.DATABUNDLES_DIR,
            f'{paths.kaldi_helpers.INPUT_PATH}/data'
        )
        self.model = Model(
            self,
            'model',
            paths.CURRENT_MODEL_DIR,
            paths.MODELS_DIR,
            paths.kaldi_helpers.INPUT_PATH
        )
        # self.transcription = Transcription(
        #     'transcription',
        #     paths.CURRENT_TRANSCRIPTION_DIR,
        #     paths.TRANSCRIPTIONS_DIR,
        #     f'{paths.kaldi_helpers.INPUT_PATH}/trans'
        # )

