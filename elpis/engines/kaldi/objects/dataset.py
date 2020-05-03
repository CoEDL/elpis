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
        self.__files: List[Path] = []
        self.pathto = DSPaths(self.path)
        self.has_been_processed = False

        # config
        self.config['has_been_processed'] = False
        self.config['files'] = []
        # It's OK to have chars in the collapse list that are also in the explode list
        # because explode will be done first, removing them from the text,
        # thus they won't match during the collapse step
        self.config['punctuation_to_collapse_by'] = string.punctuation + ",…‘’“”°"
        self.config['punctuation_to_explode_by'] = "-"

        # All tier types and names for entire dataset
        # This is also very Elan-specific!
        self.config['tier_max_count'] = 1
        self.config['tier_types'] = []
        self.config['tier_names'] = []
        self.config['tier_order'] = 1
        self.config['tier_type'] = ""
        self.config['tier_name'] = ""

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.__files = [Path(path) for path in self.config['files']]
        self.pathto = DSPaths(self.path)
        self.has_been_processed = self.config['has_been_processed']
        return self
