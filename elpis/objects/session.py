from pathlib import Path
from elpis.wrappers.utilities import hasher


class Session(object):
    def __init__(self, base_path: Path):
        self.hash = hasher.new()
        self.path = base_path.joinpath(self.hash)

    def log(self, stage_name: str, content: str):
        with open(str(self.path.joinpath('log.txt', 'a'))) as flog:
            flog.write(f'\n{f" {stage_name} ":=^{80}}\n')
            flog.write(content)
