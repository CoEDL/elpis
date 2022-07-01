import json
import time
from abc import ABC, abstractclassmethod, abstractmethod
from pathlib import Path
from elpis.engines.common.utilities import hasher

# Design constraint
# Since there are four classes that must have their states saved to the
# operating system, this single class was made to provide some common
# functionality and a standard of operation for these classes. The alternative
# to using this method of storing everything on disk (using the file system
# directly) is to implement a database, however, kaldi requires access to
# files and a specific file structure. This was the constrain that lead to the
# FSObject.


# The classes that use FSObject as a base are: Dataset, Model, Transcription
# and KaldiInterface.


class FSObject(ABC):

    """
    ..
        "... TODO More docs here ..."

    ``_config_file``
    ================
    All classes that inherit from FSObjects should implement a ``_config_file``
    static variable with the name of the JSON file that store the objects
    non-volatile properties. The ``_config_file`` file must be located in the
    ``dir_name`` directory.
    """

    _links = {}  # Used for child classes to dynamically link to other objects if applicable.

    # _config_file = '___________.json'
    # Do not uncomment line above, this is an example of how to implement the
    # _config_file variable in subclasses (classes that inherit this class).

    def __init__(
        self,
        parent_path: Path = None,
        dir_name: str = None,
        name: str = None,
        pre_allocated_hash: str = None,
    ):
        # Not allowed to instantiate this base class
        if type(self) == FSObject:
            raise NotImplementedError("Must inherit FSObject, not instantiate it.")

        # Must have a _config_file variable
        self._config_file

        # _config_file must be a JSON file
        if not self._config_file.endswith(".json"):
            raise ValueError('_config_file must be a JSON file (ends with ".json")')

        # Optional arg: pre_allocated_hash
        if pre_allocated_hash is None:
            h = hasher.new()
        else:
            h = pre_allocated_hash

        # Optional arg: dir_name
        if dir_name is None:
            dir_name = h

        # path to the object
        self.__path = Path(parent_path).joinpath(dir_name)
        self.path.mkdir(parents=True, exist_ok=True)
        #  if no config, then create it
        config_file_path = Path(f"{self.__path}/{self._config_file}")
        if not config_file_path.exists():
            self.ConfigurationInterface(self)._save({})
        if "name" not in self.config._load() or name is not None:
            self.config["name"] = name
        if "hash" not in self.config._load():
            self.config["hash"] = h
        if "date" not in self.config._load():
            self.config["date"] = str(time.time())

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
        return self

    @property
    @abstractmethod
    def _config_file(self) -> str:
        raise NotImplementedError("no _config_file has been defined for this class")

    # @property
    # @abstractmethod
    # def state(self) -> dict:
    #     raise NotImplementedError('no state has been defined for this class')

    @property
    def path(self) -> Path:
        """write protection on self.path"""
        return Path(self.__path)

    @property
    def name(self) -> str:
        return self.config["name"]

    # Must change name in the KaldiInterface object.

    @property
    def hash(self) -> str:
        return self.config["hash"]

    def __hash__(self) -> int:
        return int(f"0x{self.hash}", 0)

    @property
    def date(self):
        return self.config["date"]

    @property
    def config(self):
        return self.ConfigurationInterface(self)

    # def link(self, *link_objects):
    #     # NOTE It should be easier to use **links (keyword arguments), but it forces the edition of related endpoint file, so wait for now.
    #     print(f"*** linking of {self} to these objects: {self._links}.")
    #     for link_name, link_class in self._links.items():
    #         link_object = [link_object for link_object in link_objects if issubclass(link_object.__class__, link_class)][0]  # Do we need assert length = 1 here?
    #         setattr(self, link_name, link_object)
    #         self.config[f"{link_name}_name"] = link_object.name

    class ConfigurationInterface(object):
        """
        Continuously save changes to disk and only read properties from disk
        (in the JSON file storing the objects configuration).

        This class is more syntax sugar. Particularly so we can treat the
        'config' attribute/property in the FSObject class like a JSON
        (or dict), since it is interfacing directly with one.
        """

        def __init__(self, fsobj):
            self.fsobj = fsobj

        def _file_name(self):
            return getattr(self.fsobj, "_config_file", "config.json")

        def _load(self):
            with open(f"{self.fsobj.path}/{self._file_name()}", "r") as fin:
                return json.load(fin)

        def _save(self, conf):
            with open(f"{self.fsobj.path}/{self._file_name()}", "w") as fout:
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
