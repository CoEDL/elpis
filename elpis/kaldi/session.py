import time

from pathlib import Path

from . import hasher

class Session(object):
    def __init__(self, basepath: Path):
        self.hash = hasher.new()
        self.path = basepath.joinpath(self.hash)
    def log(self, stage_name: str, content: str):
        with open(self.path.joinpath('log.txt', 'a')) as flog:
            flog.write(f'\n{f" {stage_name} ":=^{80}}\n')
            flog.write(content)


