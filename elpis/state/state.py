import os
from typing import List, TextIO as TextFile
from ..paths import MODELS_DIR
    
    
def filter_filenames(filenames: List[str]) -> List[str]:
    return [x.split('/')[-1] for x in filenames]


class State(object):
    def __init__(self):
        super()

def load_existing_models():#[model]: #corpus?
    return []
