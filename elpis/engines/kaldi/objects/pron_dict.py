from pathlib import Path
from io import BufferedIOBase

from elpis.engines.kaldi.objects.dataset import KaldiDataset
from elpis.engines.common.objects.pron_dict import PronDict
from elpis.engines.common.input.make_prn_dict import generate_pronunciation_dictionary


class KaldiPronDict(PronDict):  # NOTE See note at import: later make a generic PronDict class.
    # The configuration settings stored in the file below.
    _config_file = 'pron_dict.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataset: KaldiDataset = None
        self.config['dataset_name'] = None  # dataset hash has not been linked
        self.l2s_path = self.path.joinpath('l2s.txt')
        self.lexicon_txt_path = self.path.joinpath('lexicon.txt') #TODO change to lexicon_txt_path
        self.config['l2s'] = None  # file has not been uploaded

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.l2s_path = self.path.joinpath('l2s.txt')
        self.lexicon_txt_path = self.path.joinpath('lexicon.txt')
        self.dataset = None
        return self

    def set_l2s_path(self, path: Path):
        path = Path(path)
        with path.open(mode='rb') as fin:
            self.set_l2s_fp(fin)

    def set_l2s_fp(self, file: BufferedIOBase):
        self.set_l2s_content(file.read())

    def set_l2s_content(self, content: str):
        # TODO: this function uses parameter str, and must be bytes or UTF-16
        self.config['l2s'] = True
        with self.l2s_path.open(mode='wb') as fout:
            fout.write(content)

    def get_l2s_content(self):
        try:
            with self.l2s_path.open(mode='r') as fin:
                return fin.read()
        except FileNotFoundError:
            return False

    def get_l2s(self):
        with self.l2s_path.open(mode='r') as fin:
            return fin.read()

    def generate_lexicon(self):
        # task make-prn-dict
        # TODO this file needs to be reflected in kaldi_data_local_dict
        generate_pronunciation_dictionary(word_list=f'{self.dataset.pathto.word_list_txt}',
                                          pronunciation_dictionary=f'{self.lexicon_txt_path}',
                                          config_file=f'{self.l2s_path}')
    # @property
    # def lexicon(self):
    #     with self.lexicon_txt_path.open(mode='rb') as fin:
    #         return fin.read()

    def get_lexicon_content(self):
        try:
            with self.lexicon_txt_path.open(mode='r') as fin:
                return fin.read()
        except FileNotFoundError:
            return 'No lexicon yet'

    def save_lexicon(self, text):
        # open pron dict file
        # write lexicon text to file
        print("lexicon", text)
        try:
            with self.lexicon_txt_path.open(mode='w') as fout:
                fout.write(text)
        except FileNotFoundError:
            return 'No lexicon yet'
