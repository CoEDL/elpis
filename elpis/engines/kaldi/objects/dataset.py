import string

from pathlib import Path
from typing import List
from elpis.engines.common.objects.dataset import Dataset, DSPaths


# TODO: this is very ELAN specific code...
DEFAULT_TIER_TYPE = 'default-lt'
DEFAULT_TIER_NAME = 'Phrase'


class KaldiDataset(Dataset):
    # TODO Code deletion: this class is mainly empty compared to its parent because I don’t know
    #  what is really Kaldi-specific.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        return self
