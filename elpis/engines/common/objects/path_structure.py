from pathlib import Path


def existing_attributes(obj):
    return set(dir(obj))


def ensure_paths_exist(obj, existing_attrs):
    post_structure_definitions = set(dir(obj))
    structure_path_attrs = post_structure_definitions - existing_attrs
    for attr in structure_path_attrs:
        path: Path = getattr(obj, attr)
        path.mkdir(parents=True, exist_ok=True)


class PathStructure(object):
    def __init__(self, parent: Path):
        self.parent = Path(parent)
        self.path: Path = self.parent.joinpath("kaldi")

        # define the kaldi working directory directory structure (no files yet)
        non_structure_attrs = set(dir(self))

        self.conf: Path = self.path.joinpath("conf")

        self.data: Path = self.path.joinpath("data")
        self.data_local: Path = self.data.joinpath("local")
        self.data_local_dict: Path = self.data_local.joinpath("dict")
        self.data_infer: Path = self.data.joinpath("infer")
        self.data_test: Path = self.data.joinpath("test")
        self.data_train: Path = self.data.joinpath("train")

        self.local: Path = self.path.joinpath("local")

        # check that the newly added directories exist
        post_structure_definitions = set(dir(self))
        structure_path_attrs = post_structure_definitions - non_structure_attrs
        for attr in structure_path_attrs:
            path: Path = getattr(self, attr)
            path.mkdir(parents=True, exist_ok=True)
