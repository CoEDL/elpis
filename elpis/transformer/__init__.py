import os
import importlib
from typing import Dict
from pathlib import Path

# WARNING: All other python files in this directory with the exception of this one should be a data transformer.

# Note: An instanciated data transformer can be used for on multiple datasets so a data transformer can be told to clean up it's variables for the next run by calling the clean_up function. can use @dt.on_cleanup to attach anything to this process.
# Note: 

class DataTransformer:
    """
    A data transformer handles the importing and exporting of data from the
    Elpis pipeline system. This class is a standard interface to 

    Variable ctx
    The context is an dictionary that stores important information closely
    accossiated with the data. For example if the file contains many tiers of
    annotation, this may include which tier to select.


    """

    # Class variable DataTransformer.transformers contains a mapping from a
    # transformer name to the unique object instance of that transformer. As
    # per dictionary rules, tranformers must be uniquely named.
    transformers = {}
    _make_transformer = {}
    @classmethod
    def get_transformer(cls, name: str):
        """
        TODO: better description
        Example:
            elan = DataTransformer.get_transformer('Elan')
        
        :returns: The data transformer belonging to the name.
        :raises:
            ValueError: if the name does not belong to any existing data transformers.
        """
        if name not in cls.transformers.keys():
            raise ValueError(f'DataTransformer with name {name} has not been created')
        return cls.transformers[name]


    def __init__(self, name):
        self._name = name
        # TODO: check if the name already exists, if so, throw an error.
        # self._can_import = True
        # self._can_export = True
        self._ctx = {}
        # self._ext_imp_hints = []
        # self._ext_exp_hints = []
        # self._import_filtered = False
        # self._import_filter_type_set = False

        self._import_ext_handlers = {}

        self._audio_ext = 'wav'


        # TODO: describe what these are: name to annotation dict, name to audio dict, must have name in both, cannot exist only in one.
        self._annotation_store = {}
        self._audio_store = []

        DataTransformer.transformers[name] = self

    # def can_import(self) -> bool:
    #     '''
    #     Reports if this data transformer can import data.
    #     :return: True if the data transformer is capable of importing,
    #             otherwise false.
    #     '''
    #     return self._can_import

    
    # def can_export(self) -> bool:
    #     '''
    #     Reports if this data transformer can export data.
    #     :return: True if the data transformer is capable of exporting,
    #             otherwise false.
    #     '''
    #     return self._can_export

    # def disable_import(self) -> None:
    #     """
    #     Disables importing functionality for this data transformer.
    #     """
    #     self._can_import = False

    # def disable_export(self) -> None:
    #     """
    #     Disables exporting functionality for this data transformer.
    #     """
    #     self._can_export = False

    # def __import(self, file_paths)

    @property
    def context(self) -> dict:
        return self._ctx
    
    @context.setter
    def context(self, ctx):
        self._ctx = ctx


    # def importer(self, f):
    #     pass
    def handle(self, *extensions):
        def decorator(f):
            def closure(paths):
                f(paths)
            if len(extensions) == 0:
                self._import_ext_handlers[None] = closure
            for extention in extensions:
                self._import_ext_handlers[extention] = closure
            return closure
        return decorator

    def add_annotation(self, name: str, annotation: Dict[str, str]):
        if name not in self._annotation_store.keys():
            self._annotation_store[name] = []
        self._annotation_store[name].append(annotation)

    def import_directory(self, path: str):
        #gather files
        file_path_to_handler = {}
        ext_to_file_path_list = {}
        for file_path in Path(path).iterdir():
            ext = file_path.name.split('.')[-1]
            if ext not in ext_to_file_path_list.keys():
                ext_to_file_path_list[ext] = [file_path]
            else:
                ext_to_file_path_list[ext].append(file_path)



# import other python files in this directory as data transformers.
names = os.listdir('elpis/transformer')
try:
    names.remove('__init__.py')
except ValueError:
    pass # '__init__.py' not in the list and that's okay.
# Only keep python files
names = [name[:-len('.py')] for name in names if name.endswith('.py')]
for importer_file_name in names:
    i = importlib.import_module('elpis.transformer.' + importer_file_name)
    print(dir(i))
    print(DataTransformer.transformers)


    # def reprocess_audio(self, audio_path: str):
    #     pass