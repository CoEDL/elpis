#!/usr/bin/python3

"""
Copyright: University of Queensland, 2019
Contributors:
              Nicholas Buckeridge - (The University of Queensland, 2019)
"""

import os
import importlib
import json
import shutil
import threading

from inspect import signature
from multiprocessing.dummy import Pool
from typing import List, Dict, Callable
from pathlib import Path

from elpis.engines.common.input.resample_audio import process_item

# A json_str is the same as a normal string except must always be deserializable into JSON as an invariant.
json_str = str

AnnotationFunction = Callable[[Dict], None]
AddAudioFunction = Callable[[str, str], None]
FileImporterType = Callable[[List[str], Dict, AnnotationFunction], None]
DirImporterType = Callable[[str, Dict, AnnotationFunction, AddAudioFunction], None]
AudioProcessingFunction = Callable[[List[str], Dict, AddAudioFunction], None]

SettingsChangeCallback = Callable[[dict, dict], None]


PathList = List[str] # a list of paths to file
FilteredPathList = Dict[str, PathList]

# WARNING: All other python files in this directory with the exception of this one should be a data transformer.

# Note: An instanciated data transformer can be used for on multiple datasets so a data transformer can be told to clean up it's variables for the next run by calling the clean_up function. can use @dt.on_cleanup to attach anything to this process.

# Audio and Annotaion data
# ========================
# Data transformers when importing a collection extract annotation data from a
# given transcription data structure and attach it to an ID. An ID is a name
# that identifies the audio resource. IDs are unique and are derived from the
# names of the audio files without the extention. Every ID will then start with
# en empty list of annotations. Import functions can then make calls to a
# callback (add_annotation) that appends an anotaion dictiornary to the IDs
# list.

def copyJSONable(obj):
    """
    Creates a copy of obj and ensures it is JSONable.

    :return: copy of obj.
    :raises:
        TypeError: if the obj is not JSONable.
    """
    return json.loads(json.dumps(obj))


class DataTransformer:
    """
    A data transformer handles the importing and exporting of data of a particular
    format from the Elpis pipeline system.

    To instanciate a data transformer (data importer/exporter), see the
    make_importer/make_exporter functions in this file.
    """

    def __init__(self,
                    name: str,
                    settings: Dict,
                    ui: List,
                    callback_get_config,
                    callback_set_config,
                    settings_change_callback: SettingsChangeCallback
                    ):

        # Varialbles to be saved between in non-volitile memory exist in the config
        config = {}

        # save the callbacks for getting/setting importer/exporter configurations
        self._callback_get_config = callback_get_config
        self._callback_set_config = callback_set_config

        # Name and UI config are immutable. Will not change after DT is created
        config['name'] = name
        config['ui'] = ui

        # settings is mutable and is stored in the dataset.config (on disk)
        config['settings'] = settings
        self._settings_change_callback = settings_change_callback # TODO: name change 'context' -> 'settings'

        # annotation_store: collection of (ID -> List[annotaion obj]) pairs
        self._annotation_store = {}
        # audio_store: collection of (ID -> audio_file_path) pairs
        self._audio_store = {}

        self._callback_set_config(config)

        self._validaters = {}
        self._ui_updater = None # Gets replaced by callback (used on file addition)
        self._extentions = []

    def process(self):
        """
        To be overriden.
        """
        pass
    
    def get_name(self) -> str:
        return self._callback_get_config()['name']

    def get_ui(self) -> Dict:
        return self._callback_get_config()['ui']
    
    # TODO: add import/export settings to the state
    def get_state(self) -> str:
        return self._callback_get_config()

    def get_settings(self):
        return self._callback_get_config()['settings']
    
    def set_setting(self, key, value):
        """
        Ensures the callback is called when the context is modified.
        TODO: improve this doc
        Ensure only settings is writable.
        """
        config = self._callback_get_config()
        settings = config['settings']
        settings[key] = value # TODO handle error if key is not already in settings.
        settings_for_callback = copyJSONable(settings) # TODO handle error if not JSONable
        self._settings_change_callback(settings_for_callback)
        config['settings'] = settings
        self._callback_set_config(config)
    
    def validate_files(self, extention: str, file_paths: Path):
        """ TODO fix up this doc"""
        """ Returns None if everything is okay, otherwise string with error message."""
        if extention not in self._validaters.keys():
            return None
        return self._validaters[extention](file_paths)

    def refresh_ui(self, file_paths):
        config = self._callback_get_config()
        ui = self._ui_updater(file_paths, config['ui'])
        config['ui'] = ui
        self._callback_set_config(config)

class DataTransformerAbstractFactory:
    """
    This Abstract Factory class instanciates DataTransformer classes on a call
    to build(). All other functions are decotators for creating methods for
    the DataTransformer being built.
    """


    # Class variable _transformer_factories contains a mapping from a
    # transformer name to the unique object factory for that transformer. As
    # per dictionary rules, tranformers must be uniquely named.
    _transformer_factories = {}

    # mapping extention to factories
    _ext_to_factory = {}

    def __init__(self, name: str):
        """
        Construct a new DataTransformerAbstractFactory. Normally one of these
        objects are made per import/export format type.

        :raises:
            ValueError: if DataTransformerAbstractFactory with name already
                exists.
        """
        self._name = name
        self._audio_extention = 'wav'
        self._default_context_already_set = False
        self._decorating_temp_dir = False

        # Ensure only one name exists per DataTransformerAbstractFactory
        if name in self._transformer_factories:
            raise ValueError(f'DataTransformerAbstractFactory with name "{name}" already exists')
        self._transformer_factories[name] = self

        # Context proxy variables to copy to the instanciated class
        self._import_settings = {}
        self._export_settings = {}

        # GUI configurations
        self._import_ui_data_config = {} # name -> {}
        self._export_ui_data_config = {}
        self._import_ui_type_config = {} # name -> type
        self._export_ui_type_config = {}
        self._import_ui_order_config = []
        self._export_ui_order_config = []
        self._import_title_count = 0
        self._export_title_count = 0

        # Concrete import/export function collection
        self._import_extension_callbacks: Dict[str, FileImporterType] = {}
        self._import_file_validator_callback: Dict[str, Callable] = {}
        self._import_directory_callback: Callable = None
        self._export_callback: Callable = None
        self._audio_processing_callback: Callable = None

        self._update_ui_callback = lambda x: None

        self._attributes = {}
        self._obj_to_attr_name = {}
    
    def set_audio_extention(self, ext: str):
        """
        Setter for the audio extention that will be used to scan for audio
        files.

        :param ext: the extention part of the file.
        """
        self._audio_extention = ext
        return

    def set_default_context(self, context: dict):
        """
        Sets the default import and export context.

        :raises:
            TypeError: if the context parameter is not JSONable.
            RuntimeError: if either the import or export context already contains values.
        """
        if self._import_settings != {}:
            raise RuntimeError('import context contains settings. Set default context at start of script')
        elif self._export_settings != {}:
            raise RuntimeError('export context contains settings. Set default context at start of script')
        elif self._default_context_already_set:
            raise RuntimeError('Have multiple calls to set_default_context, only allowed one')
        self._default_context_already_set = True

        # perform deep copy and ensures JSONability
        jcontext = json.dumps(context)
        self._import_settings = json.loads(jcontext)
        self._export_settings = json.loads(jcontext)
        return

    def get_audio_extention(self) -> str:
        return self._audio_extention

    def import_files(self, extention: str):
        """
        Python Decorator with single argument (extention).

        Store the decorated function as a callback to process files with the
        given extention. The parameter to the decorator is the file extention.
        The decorated function (f) should always have four parameters, being:
            1. List containing the file paths of all the files in the import
                directory with the specified extention.
            2. A dictionary context variable that can be used to access
                specialised settings.
            3. A callback to add annotation data to audio files.
            4. Path to a temporary directory
        
        This decorator is indended for the (audio file, transcription file)
        unique distinct pair usecase.
        
        The callback is used either when the DataTransformer process() function
        is called or the if the function is called directly from the
        DataTransformer object. If called directly, then only the file_paths
        argument should be passed to the function as the DataTransformer
        automatically passes context and the add_annotation callback.

        This decorator cannot be used with the import_directory decorator.

        :param extention: extention to map the callback (decorated function) to.
        :return: a python decorator
        :raises:
            RuntimeError: if import_directory is already used.
            RuntimeError: if the extention is aleady registers.
            NameError: if the decorated function name is repeated or invalid.
            RuntimeError: if the decorated function does not have three parameters.
        """
        if self._import_directory_callback is not None:
            raise RuntimeError('import_directory used, therefore cannot use import_files')
        elif extention in self._import_extension_callbacks:
            raise RuntimeError(f'"{extention}" has already been registered with import_files decorator')

        self._ext_to_factory[extention] = self._name

        def decorator(f: Callable):
            if f.__name__ in self._attributes:
                raise NameError('bad function name. Already used')
            if f.__name__ in dir(DataTransformer):
                raise NameError('bad function name. Name is attribute of DataTransformer')

            sig = signature(f)
            if len(sig.parameters) != 4:
                raise RuntimeError(f'import function "{f.__name__}" must have four parameters, currently has {len(sig.parameters)}')

            # Store the closure by file extention
            self._import_extension_callbacks[extention] = f
            # Store attribute
            self._attributes[f.__name__] = f
            self._obj_to_attr_name[f] = f.__name__
            return f
        return decorator

    def validate_files(self, extention: str):
        # TODO: Docs
        if self._import_directory_callback is not None:
            raise RuntimeError('import_directory used, therefore cannot use validate_files')
        elif extention in self._import_file_validator_callback:
            raise RuntimeError(f'"{extention}" has already been registered with validate_files decorator')

        def decorator(f: Callable):
            if f.__name__ in self._attributes:
                raise NameError('bad function name. Already used')
            if f.__name__ in dir(DataTransformer):
                raise NameError('bad function name. Name is attribute of DataTransformer')

            sig = signature(f)
            if len(sig.parameters) != 1:
                raise RuntimeError(f'validation function "{f.__name__}" must have one parameter (file_paths), currently has {len(sig.parameters)}')

            # Store the closure by file extention
            self._import_file_validator_callback[extention] = f
            # Store attribute
            self._attributes[f.__name__] = f
            self._obj_to_attr_name[f] = f.__name__
            return f
        return decorator

    def update_ui(self, f):
        self._update_ui_callback = f
        return f

    def import_directory(self, f: Callable):
        """
        Python Decorator (no arguments)

        Store the decorated function as a callback to process files of the
        given type. The decorated function (f) should always have five
        parameters, being:
            1. Directory path containing files/directories of interest.
            2. A Dictionary context variable that can be used to access
                specialised settings.
            3. A callback to add annotaion data to audio files.
            4. A callback to add audio files.
            5. Path to a temporary directory.
        
        The callback is used either when the DataTransformer process() function
        is called or the if the function is called directly (without passing
        patameters) from the DataTransformer object.

        This decorator cannot be used with the import_file decorator.

        :return: the function
        :raises:
            RuntimeError: if the callback has already been specified.
            RuntimeError: if import_files had already been specified.
            RuntimeError: if the decorated function name is repeated or invalid.
            RuntimeError: if the decorated function does not have four parameters.
        """
        if self._import_directory_callback is not None:
            raise RuntimeError('import_directory already specified')
        if len(self._import_extension_callbacks) != 0:
            raise RuntimeError('import_files used, therefore cannot use import_directory')
        if f.__name__ in self._attributes:
            raise NameError('bad function name. Already used')
        if f.__name__ in dir(DataTransformer):
            raise NameError('bad function name. Name is attribute of DataTransformer')

        sig = signature(f)
        if len(sig.parameters) != 5:
            raise RuntimeError(f'import function "{f.__name__}" must have five parameters, currently has f{len(sig.parameters)}')
        
        # Store the closure by file extention
        self._import_directory_callback = f
        self._attributes[f.__name__] = f
        self._obj_to_attr_name[f] = f.__name__
        return f

    def export(self, f: Callable):
        """
        Python Decorator (no arguments).

        Store the decorated function as a callback to export a transcription
        file given an audio file.
        The decorated function (f) should always have four parameters, being:
            1. Annotataions dictionary.
            2. A dictionary context variable that can be used to access
                specialised settings.
            3. Output directory.
            4. Path to a temporary directory
        
        This decorator is indended for the (audio file, transcription file)
        unique distinct pair usecase.
        
        The callback is used by directly calling it from the DataTransformer
        object. If called directly, then only the annotations and the
        output_dir arguments should be passed to the function as the
        DataTransformer automatically passes context.

        :return: the function
        :raises:
            RuntimeError: if export is already used.
            RuntimeError: if the decorated function name is repeated or invalid.
            RuntimeError: if the decorated function does not have three parameters.
        """
        if self._export_callback != None:
            raise RuntimeError('export used, therefore cannot use export')
        if f.__name__ in self._attributes:
            raise NameError('bad function name. Already used')
        if f.__name__ in dir(DataTransformer):
            raise NameError('bad function name. Name is attribute of DataTransformer')

        sig = signature(f)
        if len(sig.parameters) != 4:
            raise RuntimeError(f'export function "{f.__name__}" must have four parameters, currently has f{len(sig.parameters)}')
        self._attributes[f.__name__] = f
        self._export_callback = f
        self._obj_to_attr_name[f] = f.__name__
        return f
    
    def _type_to_str(self, t):
        if t == str:
            return 'str'
        if t == int:
            return 'int'
        if isinstance(t, list):
            # TODO: check the types in t
            return t
        print("t:", t, ":", type(t), ': t is list =', t is list, ": type(t) == list = ", type(t) == list)
        raise ValueError(f'type \'{t}\' is not a valid type')

    def import_setting(self, key, type, default=None, display_name=None, description=None):
        """
        Add a field to the import context.

        :param key: the name of the field. TODO: change 'key' -> 'name'
        :param type: the type of the field (must be JSONable)
        :param default: (Optional) default value of the field.
        TODO: add display name
        :param ui: (Optional) ui configuration TODO: replace with description
        :raises:
            RuntimeError: if the key has already been specified as an import setting or in the default context.
        """
        if key in self._import_settings:
            raise ValueError(f'key "{key}" already in the import context')
        self._import_settings[key] = default
        self._import_ui_data_config[key] = {
            'type': self._type_to_str(type),
            'display_name': display_name,
            'description': description
        }
        self._import_ui_type_config[key] = 'setting'
        self._import_ui_order_config.append(key)
    
    def export_setting(self, key, type, default=None, display_name=None, description=None):
        """
        Add a field to the export context.

        :param key: the name of the field.
        :param type: the type of the field (must be JSONable)
        :param default: (Optional) default value of the field.
        TODO: add display name
        :param ui: (Optional) ui configuration TODO: replace with description
        :raises:
            RuntimeError: if the key has already been specified as an export setting or in the default context.
        """
        if key in self._export_settings:
            raise ValueError(f'key "{key}" already in the export context')
        self._export_settings[key] = default
        self._export_ui_data_config[key] = {
            'type': self._type_to_str(type),
            'display_name': display_name,
            'description': description
        }
        self._export_ui_type_config[key] = 'setting'
        self._export_ui_order_config.append(key)
    
    def import_setting_title(self, title):
        key = '_title_' + str(self._import_title_count)
        self._import_title_count += 1
        self._import_ui_data_config[key] = { 'title': title }
        self._import_ui_type_config[key] = 'title'
        self._import_ui_order_config.append(key)
        return
        
    def export_setting_title(self, title):
        key = '_title_' + str(self._export_title_count)
        self._export_title_count += 1
        self._export_ui_data_config[key] = { 'title': title }
        self._export_ui_type_config[key] = 'title'
        self._export_ui_order_config.append(key)
        return
        
    def general_setting_title(self, title):
        self.import_setting_title(title)
        self.export_setting_title(title)
        return

    def general_setting(self, key, type, default=None, display_name=None, description=None):
        """
        Add a field to the both import and export context.

        :param key: the name of the field.
        :param type: the type of the field (must be JSONable)
        :param default: (Optional) default value of the field.
        TODO: add display name
        :param ui: (Optional) ui configuration TODO: replace with description
        :raises:
            RuntimeError: if the key has already been specified as an import or export setting, or in the default context.
        """
        if key in self._import_settings:
            raise ValueError(f'key "{key}" already in the import context')
        if key in self._export_settings:
            raise ValueError(f'key "{key}" already in the export context')
        self.import_setting(key, type, default=default, display_name=display_name, description=description)
        self.export_setting(key, type, default=default, display_name=display_name, description=description)
    
    def is_import_capable(self):
        if self._import_directory_callback != None:
            return True
        if len(self._import_extension_callbacks) != 0:
            return True
        return False
    
    def is_export_capable(self):
        return self._export_callback != None

    def replace_reprocess_audio(self, f):
        """"""
        if self._audio_processing_callback != None:
            raise RuntimeError('replace_reprocess_audio can only be specified once')
        self._audio_processing_callback = f
        return f

    def build_importer(self,
                        collection_path: str,
                        resampled_path: str,
                        temporary_directory_path: str,
                        transcription_json_file_path: str,
                        get_config_callback,
                        set_config_callback,
                        settings_change_callback: SettingsChangeCallback
                    ) -> DataTransformer:

        # check arguments
        if not Path(collection_path).is_dir():
            raise RuntimeError('path to collection does not exist')
        if not Path(resampled_path).is_dir():
            raise RuntimeError('path to the resampled directory does not exist')
        if not Path(temporary_directory_path).is_dir():
            raise RuntimeError('path to temporary directory does not exist')

        # Prepare a copy of the context object.
        settings = copyJSONable(self._import_settings)

        # Prepare the UI
        ui = {
            "data": self._import_ui_data_config,
            "type": self._import_ui_type_config,
            "order": self._import_ui_order_config
        }

        dt = DataTransformer(
            self._name,
            settings,
            ui,
            get_config_callback,
            set_config_callback,
            settings_change_callback
        )

        # Callbacks to add data to the internal stores
        def add_annotation(id, obj):
            nonlocal dt
            # check the object type
            if type(obj) != dict:
                raise TypeError('annotation top level variable must be a dictionary')
            fields = { 'audio_file_name', 'transcript', 'start_ms', 'stop_ms' }
            if set(obj.keys()) != fields:
                raise TypeError('annotation object contains an incorrect field name')
            # add the annotation
            if id in dt._annotation_store:
                dt._annotation_store[id].append(obj)
            else:
                dt._annotation_store[id] = [obj]
            return # from add_annotation
        add_audio = lambda id, audio_path: dt._audio_store.update({id: audio_path})

        # Make attributes for dt to be called directly.
        if self._import_directory_callback != None:
            # Make wrapper for import_directory_callback
            f = self._import_directory_callback
            def wrapper():

                nonlocal dt
                nonlocal f
                nonlocal collection_path
                nonlocal add_annotation
                nonlocal add_audio
                nonlocal temporary_directory_path
                return f(
                    collection_path,
                    # resampled_path, # TODO: this line needs to be here so add the parameter to tests
                    copyJSONable(dt.get_settings()),
                    add_annotation,
                    add_audio,
                    temporary_directory_path
                )
            setattr(dt, self._obj_to_attr_name[f], wrapper)
            # Construct the process function
            obj_to_attr_name = self._obj_to_attr_name
            def import_directory_process():
                # do not reference self in this closure
                nonlocal dt
                nonlocal collection_path
                nonlocal resampled_path
                nonlocal add_annotation
                nonlocal add_audio
                nonlocal temporary_directory_path
                nonlocal f
                nonlocal obj_to_attr_name

                # import directory contents
                callback_name = obj_to_attr_name[f]
                callback = getattr(dt, callback_name)
                callback()

                # save transcription data to file
                with Path(transcription_json_file_path).open(mode='w') as fout:
                    annotations = []
                    for id in dt._annotation_store:
                        annotations.extend(dt._annotation_store[id])
                    fout.write(json.dumps(annotations))
                return # import_directory_process
            setattr(dt, 'process', import_directory_process) # Override this function
        else:
            # make wrapper for import_files (accepts one argument)
            for _ext, f in self._import_extension_callbacks.items():
                def wrapper(file_paths: str):
                    """
                    Attribute that is assigned to the DataTransformer. This
                    Handler must only import the given files.
                    """
                    nonlocal dt
                    nonlocal f
                    nonlocal add_annotation
                    nonlocal temporary_directory_path
                    return f(
                        file_paths,
                        copyJSONable(dt.get_settings()),
                        add_annotation,
                        temporary_directory_path
                    )
                setattr(dt, self._obj_to_attr_name[f], wrapper)
            # Construct the process function
            audio_processing_callback = self._audio_processing_callback
            if audio_processing_callback == None:
                audio_processing_callback = _default_audio_resampler
            import_extension_callbacks = self._import_extension_callbacks
            audio_extention = self._audio_extention
            def import_files_process():
                """
                Handler that is set to the .process() function.
                """
                # do not reference self in this closure
                nonlocal dt
                nonlocal collection_path
                nonlocal resampled_path
                nonlocal add_annotation
                nonlocal add_audio
                nonlocal temporary_directory_path
                nonlocal audio_processing_callback
                nonlocal import_extension_callbacks
                nonlocal audio_extention

                extention_to_files: FilteredPathList = _filter_files_by_extention(collection_path)

                # process audio
                if audio_extention in extention_to_files: # skip if there are no audio files to process
                    audio_paths: PathList = extention_to_files.pop(audio_extention)
                    audio_processing_callback(audio_paths, resampled_path, add_audio, temporary_directory_path)

                # process transcription data
                for extention, file_paths in extention_to_files.items():
                    # only process the file type collection if a handler exists for it
                    callback = import_extension_callbacks.get(extention, None)
                    if callback is not None:
                        callback(file_paths, dt.get_settings(), add_annotation, temporary_directory_path)

                # save transcription data to file
                with Path(transcription_json_file_path).open(mode='w') as fout:
                    annotations = []
                    for id in dt._annotation_store:
                        annotations.extend(dt._annotation_store[id])
                    fout.write(json.dumps(annotations))
                return # import_files_process
            setattr(dt, 'process', import_files_process) # Override this function

        # add validators
        for ext, f in self._import_file_validator_callback.items():
            dt._validaters[ext] = f
        
        # Add ui refresher
        dt._ui_updater = self._update_ui_callback

        # Add handable extentions
        dt._extentions = self._import_file_validator_callback.keys()

        return dt
    
    def build_exporter(self,
                        path_to_ctm_file: str,
                        path_to_audio_file: str,
                        path_to_output_file: str,
                        temporary_directory_path: str,
                        get_config_callback,
                        set_config_callback,
                        settings_change_callback: SettingsChangeCallback
                    ) -> DataTransformer:
        # Prepare a copy of the context object.
        settings = json.loads(json.dumps(self._export_settings))

        # Prepare the UI
        ui = {
            "data": self._export_ui_data_config,
            "type": self._export_ui_type_config,
            "order": self._export_ui_order_config
        }

        dt = DataTransformer(
            self._name,
            settings,
            ui,
            get_config_callback,
            set_config_callback,
            settings_change_callback
        )
        return dt

def _default_settings_change_callback(settings):
    pass

def make_importer(name: str,
                    collection_path: str,
                    resampled_path: str,
                    temporary_directory_path: str,
                    transcription_json_file_path: str,
                    get_config_callback,
                    set_config_callback,
                    settings_change_callback=_default_settings_change_callback

                ) -> DataTransformer:
    if name not in DataTransformerAbstractFactory._transformer_factories:
        raise ValueError(f'data transformer factory with name "{name}" not found')
    dtaf: DataTransformerAbstractFactory = DataTransformerAbstractFactory._transformer_factories[name]
    if not dtaf.is_import_capable():
        raise ValueError(f'data transformer factory with name "{name}" cannot import')
    dt = dtaf.build_importer(
        collection_path,
        resampled_path,
        temporary_directory_path,
        transcription_json_file_path,
        get_config_callback,
        set_config_callback,
        settings_change_callback
    )
    return dt

def make_exporter(name: str,
                    collection_path: str,
                    resampled_path: str,
                    temporary_directory_path: str,
                    transcription_json_file_path: str,
                    get_config_callback,
                    set_config_callback,
                    settings_change_callback=_default_settings_change_callback
                ) -> DataTransformer:
    if name not in DataTransformerAbstractFactory._transformer_factories:
        raise ValueError(f'data transformer factory with name "{name}" not found')
    dtaf: DataTransformerAbstractFactory = DataTransformerAbstractFactory._transformer_factories[name]
    if not dtaf.is_export_capable():
        raise ValueError(f'data transformer factory with name "{name}" cannot export')
    dt = dtaf.build_exporter(
        collection_path,
        resampled_path,
        temporary_directory_path,
        transcription_json_file_path,
        get_config_callback,
        set_config_callback,
        settings_change_callback
    )
    return dt

def _filter_files_by_extention(dir_path: str) -> Dict[str, List[str]]:
    """
    Separate all files into lists by file extention.

    :param dir_path: Filesystem path to contents directory.
    :return: Dictionary of extentions as keys and lists of assocciated paths as values.
    """
    dir_path = Path(dir_path)
    extention_to_files = {}
    for file_path in dir_path.iterdir():
        if '.' not in file_path.name:
            # skip extentionless files
            continue
        if file_path.is_dir():
            # skip directories
            continue
        extention = file_path.name.split('.')[-1]
        # Make dictionary of files separated by 
        if extention not in extention_to_files:
            extention_to_files[extention] = [f'{file_path}']
        else:
            extention_to_files[extention].append(f'{file_path}')
    return extention_to_files

def _default_audio_resampler(audio_paths: List[str], resampled_dir_path: str, add_audio: AddAudioFunction, temp_dir_path: str):
    """
    A default audio resampler that converts any media accepted by sox to a
    standard format specified in process_item.

    :param audio_paths: list of paths to audio files to resample.
    :param resampled_dir_path: path to a directory to save the resampled files to.
    :param add_audio: callback to register the audio with the importer.
    :param temp_dir_path: path to a temporary directory, will exist before the
        function runs and will be deleted immediately after the function ends.
        Must be the last parameter as this path is prepended on build().
    """
    
    temp_dir_path = Path(temp_dir_path)
    resampled_dir_path = Path(resampled_dir_path)

    # Empty resampled contents
    if resampled_dir_path.exists():
        shutil.rmtree(f'{resampled_dir_path}')
    resampled_dir_path.mkdir(parents=True, exist_ok=True)

    process_lock = threading.Lock()
    temporary_directories = set()
    map_arguments = [(index, audio_path, process_lock, temporary_directories, temp_dir_path)
                        for index, audio_path in enumerate(audio_paths)]
    # Multi-Threaded Audio Re-sampling
    with Pool() as pool:
        outputs = pool.map(process_item, map_arguments)
        for audio_file in outputs:
            shutil.move(audio_file, resampled_dir_path)
            file_name = Path(audio_file).name
            id = '.'.join(file_name.split('.')[:-1])
            resampled_file_path = f'{resampled_dir_path.joinpath(file_name)}'
            add_audio(id, resampled_file_path)

# import other python files in this directory as data transformers.
def _import_instanciated_data_transformers():
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
        print(DataTransformerAbstractFactory._transformer_factories)
_import_instanciated_data_transformers()
