import json
import time
from pathlib import Path
from elpis.wrappers.utilities import hasher
from elpis.wrappers.objects.logger import Logger

# Desing constraint
# Since there are four classes that must have their states saved to the
# operating system, this single class was made to provide some common
# functionality and a standard of operation for these classes. The alternative
# to using this method of storing everything on disk (using the file system
# directly) was to implement a database, however, kaldi required access to
# files and a specific file structure. This was the constrain that lead to the FSObject.

# The classes that use FSObject as a base are: Dataset, Model, Transcription
# and KaldiInterface.


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
        self.config['date'] = str(time.time())

        if logger is None:
            self.config['logger'] = None
        else:
            self.config['logger'] = logger.hash

    def _initial_config(self, config):
        self.ConfigurationInterface(self)._save(config)

    @classmethod
    def load(cls, base_path: Path):
        """
        Create the proxy FSObject from an existing one in the file-system.

        :param base_path: is the path to the FSObject representation.
        :return: an instansiated FSObject proxy.
        """
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
    def date(self):
        return self.config['date']

    @property
    def config(self):
        return self.ConfigurationInterface(self)

    class ConfigurationInterface(object):
        """
        Continuesly save changes to disk and only read properties from disk
        (in the JSON file storing the objects configuration).

        This class is more syntax sugar. Particularly so we can treat the
        'config' attribute/property in the FSObject class like a JSON
        (or dict), since it is interfacing directly with one.
        """
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
