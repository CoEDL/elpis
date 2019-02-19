from pathlib import Path

class KaldiPathStructure(object):
    def __init__(self, parent: Path):
        self.parent = Path(parent)
        self.path: Path = self.parent.joinpath('kaldi')

        # define the kaldi working directory directory structure (no files yet)
        non_structure_attrs = set(dir(self))

        self.conf: Path = self.path.joinpath('conf')

        self.data: Path = self.path.joinpath('data')
        self.data_local: Path = self.data.joinpath('local')
        self.data_local_dict: Path = self.data_local.joinpath('dict')
        self.data_infer: Path = self.data.joinpath('infer')
        self.data_test: Path = self.data.joinpath('test')
        self.data_train: Path = self.data.joinpath('train')
        
        self.local: Path = self.path.joinpath('local')

        # check that the newly added directories exist
        post_structure_defintions = set(dir(self))
        structure_path_attrs = post_structure_defintions - non_structure_attrs
        for attr in structure_path_attrs:
            path: Path = getattr(self, attr)
            path.mkdir(parents=True, exist_ok=True)
