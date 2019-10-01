import os
import importlib
from typing import Dict

class DataTransformer:
    """
    A data transformer handles the importing and exporting of data from the
    Elpis pipeline system.

    Variable ctx
    The context is an dictionary that stores important information closely
    accossiated with the data. For example if the file contains many tiers of
    annotation, this may include which tier to select.


    """

    # Class variable DataTransformer.transformers contains a mapping from a
    # transformer name to the unique object instance of that transformer. As
    # per dictionary rules, tranformers must be uniquely named.
    transformers = {}

    def __init__(self, name):
        self._name = name
        # TODO: check if the name already exists, if so, throw an error.
        self._can_import = True
        self._can_export = True
        self._ctx = {}
        self._ext_imp_hints = []
        self._ext_exp_hints = []
        self._import_filtered = False
        self._import_filter_type_set = False


        # TODO: describe what these are: name to annotation dict, name to audio dict, must have name in both, cannot exist only in one.
        self._annotation_store = {}
        self._audio_store = []

    def can_import(self) -> bool:
        '''
        Reports if this data transformer can import data.
        :return: True if the data transformer is capable of importing,
                otherwise false.
        '''
        return self._can_import

    
    def can_export(self) -> bool:
        '''
        Reports if this data transformer can export data.
        :return: True if the data transformer is capable of exporting,
                otherwise false.
        '''
        return self._can_export

    def disable_import(self) -> None:
        """
        Disables importing functionality for this data transformer.
        """
        self._can_import = False

    def disable_export(self) -> None:
        """
        Disables exporting functionality for this data transformer.
        """
        self._can_export = False

    # def __import(self, file_paths)

    @property
    def context(self) -> dict:
        return self._ctx
    
    @context.setter
    def context(self, ctx):
        self._ctx = ctx


    def importer(self, f):
        pass
    def importer_for(self, *args):
        def decorator(f):
            def wrapped_f(*args):
                f(*args)
            return wrapped_f
        return decorator

    def add_annotation(self, name: str, annotation: Dict[str, str]):
        if name not in self._annotation_store.keys():
            self._annotation_store[name] = []
        self._annotation_store[name].append(annotation)
        
    

# print('AHHH!')
# names = os.listdir('importers')
# print('names:', names)

# try:
#     names.remove('__init__.py')
# except ValueError:
#     pass # '__init__.py' not in the list and that's okay.
# # Only keep python files
# names = [name[:-len('.py')] for name in names if name.endswith('.py')]

# print('resulting importers:', names)

# # Map name to importer object.
# importers = {}

# for importer_file_name in names:
#     i = importlib.import_module('importers.' + importer_file_name)
#     print(dir(i))