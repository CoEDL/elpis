import os
from pathlib import Path
from io import BufferedIOBase
from typing import Dict, List
from elpis.engines.common.objects.dataset import Dataset
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.input.make_prn_dict import generate_pronunciation_dictionary


class PronDict(FSObject):
    # The configuration settings stored in the file below.
    _config_file = 'pron_dict.json'
    _links = {**FSObject._links, **{"dataset": Dataset}}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset: Dataset = None
        self.config['dataset'] = None  # dataset hash has not been linked # TODO: change 'dataset' to 'dataset_name'
        self.l2s_path = self.path.joinpath('l2s.txt')
        self.lexicon_txt_path = self.path.joinpath('lexicon.txt') #TODO change to lexicon_txt_path
        self.config['l2s'] = False  # file has not been uploaded
        self.config['lexicon'] = False  # file has not been generated

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.l2s_path = self.path.joinpath('l2s.txt')
        self.lexicon_txt_path = self.path.joinpath('lexicon.txt')
        self.dataset = None
        return self

    @property
    def state(self):
        """
        An API fiendly state representation of the object.

        Invariant: The returned object can be converted to JSON using json.load(...).

        :returns: the objects state.
        """
        return {
            'name': self.config['name'],
            'hash': self.config['hash'],
            'date': self.config['date'],
            'l2s': self.config['l2s'],
            'lexicon': self.config['lexicon'],
            'dataset': self.config['dataset']
        }

    def link(self, dataset: Dataset):
        self.dataset = dataset
        self.config['dataset'] = dataset.name
        self.config['dataset_name'] = dataset.name

    def set_l2s_path(self, path: Path):
        path = Path(path)
        with path.open(mode='rb') as fin:
            self.set_l2s_fp(fin)

    def set_l2s_fp(self, file: BufferedIOBase):
        self.set_l2s_content(file.read())
        self.config['l2s'] = True

    def set_l2s_content(self, content: bytes):
        tmp_l2s_path = self.path.joinpath('tmp_l2s.txt')
        with tmp_l2s_path.open(mode='wb') as fout:
            fout.write(content)
        # translate line endings from Win to Unix for Kaldi
        with tmp_l2s_path.open(mode='r') as file_raw, self.l2s_path.open(mode='w', encoding='utf-8') as file_translated:
            file_translated.write(file_raw.read().replace('\r\n', '\n'))
        if os.path.exists(tmp_l2s_path):
            os.remove(tmp_l2s_path)
        self.config['l2s'] = True

    def build_l2s_file(self, mappings: List[Dict[str, str]]):
        with self.l2s_path.open(mode='w', encoding='utf-8') as l2s_file:
            for pair in mappings:
                l2s_file.write(f'{pair["letter"]} {pair["sound"]}\n')
        self.config['l2s'] = True

    def get_l2s_content(self):
        try:
            with self.l2s_path.open(mode='r') as fin:
                return fin.read()
        except FileNotFoundError:
            return False

    def get_l2s_pairs(self):
        """
        Returns dictionary of l2s pairs contained within the l2s file, if it exists.
        """
        pairs = []
        
        try:
            with self.l2s_path.open(mode='r') as fin:
                for line in fin:
                    if line.startswith('#'):
                        # Ignore commented lines
                        continue
                    values = line.split()
                    if len(values) > 1:
                        pairs.append({
                            "letter": values[0],
                            "sound": values[1]
                        })
        except FileNotFoundError:
            return []
        
        return pairs
        

    def generate_lexicon(self):
        # task make-prn-dict
        # TODO this file needs to be reflected in kaldi_data_local_dict
        if self.dataset == None:
            raise RuntimeError('must link dataset before generateing lexicon')
        if self.dataset.has_been_processed == False:
            raise RuntimeError('must process dataset before generateing lexicon')
        if self.config['l2s'] == False:
            raise RuntimeError('must set letters to sound before generating lexicon')
        generate_pronunciation_dictionary(word_list=f'{self.dataset.pathto.word_list_txt}',
                                          pronunciation_dictionary=f'{self.lexicon_txt_path}',
                                          config_file=f'{self.l2s_path}')
        self.config['lexicon'] = True
    @property
    def lexicon(self):
        with self.lexicon_txt_path.open(mode='rb') as fin:
            return fin.read()

    def get_lexicon_content(self):
        try:
            with self.lexicon_txt_path.open(mode='r') as fin:
                return fin.read()
        except FileNotFoundError:
            return 'No lexicon yet'

    def save_lexicon(self, bytestring):
        # open pron dict file
        # write lexicon text to file
        try:
            with self.lexicon_txt_path.open(mode='w') as fout:
                fout.write(bytestring)
            self.config['lexicon'] = True
        except FileNotFoundError:
            return 'No lexicon yet'
