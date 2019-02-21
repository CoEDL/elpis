import json
from pathlib import Path
from . import hasher
from .logger import Logger


class FSObject(object):
    def __init__(self,
                 parent_path: Path = None,
                 dir_name: str = None,
                 name: str = None,
                 logger: Logger = None,
                 pre_allocated_hash: str = None
                 ):
        if pre_allocated_hash is None:
            h = hasher.new()
        else:
            h = pre_allocated_hash
        if dir_name is None:
            dir_name = h

        # path to the object
        self.__path = Path(parent_path).joinpath(dir_name)
        self.path.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        self.ConfigurationInterface(self)._save({})
        self.config['name'] = name
        self.config['hash'] = h

        if logger is None:
            self.config['logger'] = None
        else:
            self.config['logger'] = logger.hash

    def _initial_config(self, config):
        self.ConfigurationInterface(self)._save(config)

    @classmethod
    def load(cls, base_path: Path):
        self = cls.__new__(cls)
        self.__path = Path(base_path)
        self.logger = None # TODO: use get_logger when implemented
        return self

    @property
    def path(self) -> Path:
        """write protection on self.path"""
        return Path(self.__path)

    @property
    def name(self) -> str:
        return self.config['name']

    @name.setter
    def name(self, value: str):
        self.config['name'] = value

    @property
    def hash(self) -> str:
        return self.config['hash']

    def __hash__(self) -> int:
        return int(f'0x{self.hash}', 0)

    @property
    def config(self):
        return self.ConfigurationInterface(self)

    class ConfigurationInterface(object):
        def __init__(self, fsobj):
            self.fsobj = fsobj

        def _file_name(self):
            return getattr(self.fsobj, '_config_file', 'config.json')

        def _load(self):
            with open(f'{self.fsobj.path}/{self._file_name()}', 'r') as fin:
                return json.load(fin)

        def _save(self, conf):
            with open(f'{self.fsobj.path}/{self._file_name()}', 'w') as fout:
                return json.dump(conf, fout)

        def __getitem__(self, key: str):
            return self._load()[key]

        def __setitem__(self, key, value):
            config = self._load()
            config[key] = value
            self._save(config)

        def __repr__(self):
            return self._load().__repr__()

        def __str__(self):
            return self._load().__str__()
