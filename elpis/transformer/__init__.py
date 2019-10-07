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

from multiprocessing.dummy import Pool
from typing import List, Dict, Callable
from pathlib import Path

from elpis.wrappers.input.resample_audio import process_item

# A json_str is the same as a normal string except must always be deserializable into JSON as an invariant.
json_str = str

AnnotationFunction = Callable[[Dict], None]
AddAudioFunction = Callable[[str, str], None]
FileImporterType = Callable[[List[str], Dict, AnnotationFunction], None]
DirImporterType = Callable[[str, Dict, AnnotationFunction, AddAudioFunction], None]
AudioProcessingFunction = Callable[[List[str], Dict, AddAudioFunction], None]


PathList = List[str] # a list of paths to file
FilteredPathList = Dict[str, PathList]

# WARNING: All other python files in this directory with the exception of this one should be a data transformer.

# Note: An instanciated data transformer can be used for on multiple datasets so a data transformer can be told to clean up it's variables for the next run by calling the clean_up function. can use @dt.on_cleanup to attach anything to this process.
# Note: 

# Audio and Annotaion data
# ========================
# Data transformers when importing a collection extract annotation data from a
# given transcription data structure and attach it to an ID. An ID is a name
# that identifies the audio resource. IDs are unique and are derived from the
# names of the audio files without the extention. Every ID will then start with
# en empty list of annotations. Import functions can then make calls to a
# callback (add_annotation) that appends an anotaion dictiornary to the IDs
# list.

class Functional:
    """Support class to keep a reference to an object containing a function."""
    def __init__(self, f):
        self._callback = f

    def __call__(self, *args, **kwargs):
        self._callback(*args, **kwargs)

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, f):
        self._callback = f


class DataTransformer:
    """
    A data transformer handles the importing and exporting of data from the
    Elpis pipeline system.
    """

    def __init__(self, context: Dict, collection_path: str, resampled_path: str, temporary_directory_path: str, importing_function: DirImporterType, audio_processing_callback: AudioProcessingFunction):
        self._context: Dict = context

        # Path to directory containing original audio and transcription files
        self._collection_path: str = collection_path # TODO: Remove this line

        # Path to directory containing resampled audio files
        self._resampled_path: str = resampled_path

        # Path to a temporary directory for generic use. Intended uses include
        # resampled files and processing exported data. After construction,
        # the temporary directory will exist and be empty. Etiquette to using
        # this directory is to use the _clean_tmp_dir function after each use
        # of the temporary directory.
        self._temporary_directory_path: str = temporary_directory_path
        self._clean_tmp_dir() # ensure it exists and is empty

        # Callback to transcription data importing function, requires contents
        # directoru, contect and add_annotation parameters.
        self._importing_function: DirImporterType = importing_function

        # Target media audio file extention
        self._audio_ext_filter: str = 'wav' # default to wav

        # Callback to audio importing function.
        self._audio_processing_callback: AudioProcessingFunction = audio_processing_callback

        # annotation_store: collection of (ID -> List[annotaion obj]) pairs
        self._annotation_store = {}
        # audio_store: collection of (ID -> audio_file_path) pairs
        self._audio_store = {}

    def process(self):
        self._importing_function(self, self._context)
    
    def _clean_tmp_dir(self):
        """
        Deletes and remakes the temporary directory.
        """
        path = Path(self._temporary_directory_path)
        if path.exists():
            shutil.rmtree(self._temporary_directory_path)
        path.mkdir(parents=True)





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

    def __init__(self, name: str):
        """
        :raises:
            ValueError: if DataTransformerAbstractFactory with name already
                exists.
        """

        # Proxy variables to copy to the instanciated class
        self._default_context: json_str = "{}" #JSONable

        # Abstract functions
        self._import_extension_callbacks: Dict[str, FileImporterType] = {}
        self._import_directory_callback: Callable = None

        self._functions_using_tempdir: List[Functional] = []

        if name in self._transformer_factories:
            raise ValueError(f'DataTransformerAbstractFactory with name "{name}" already exists')
        self._transformer_factories[name] = self

    def import_files(self, extention: str):
        """
        Python Decorator with single argument (extention).

        Store the decorated function as a callback to process files of the
        given type. The parameter to the decorator is the file extention. The
        decorated function (f) should always have three parameters, being:
            1. List containing the file paths of all the files in the import
                directory with the specified extention.
            2. A Dictionary context variable that can be used to access
                specialised settings.
            3. A Callback to add annotaion data to audio files.
        
        This decorator is indended for the (audio file, transcription file)
        unique distinct pair usecase.
        
        The callback is used either when the DataTransformer process() function
        is called or the if the function is called directly from the
        DataTransformer object.

        This decorator cannot be used with the import_directory decorator.

        :param extention: extention to map the callback (decorated function) to.
        :return: a python decorator
        :raises:
            RuntimeError: if import_directory is already used.
        """
        if self._import_directory_callback is not None:
            raise RuntimeError('import_directory used, therefore cannot use import_files')

        def decorator(f):
            # The closure enforces arguments.
            def closure(file_paths: List[str],
                        context: Dict,
                        add_annotation: AnnotationFunction):
                return f(file_paths, context, add_annotation)
            # Store the closure by file extention
            self._import_extension_callbacks[extention] = closure
            return closure
        return decorator
    
    def import_directory(self, f):
        """
        Python Decorator (no arguments)

        Store the decorated function as a callback to process files of the
        given type. The decorated function (f) should always have four
        parameters, being:
            1. Directory path containing files/directories of interest.
            2. A Dictionary context variable that can be used to access
                specialised settings.
            3. A callback to add annotaion data to audio files.
            4. A callback to add audio files.
        
        The callback is used either when the DataTransformer process() function
        is called or the if the function is called directly from the
        DataTransformer object.

        This decorator cannot be used with the import_file decorator.

        :return: a python decorator
        :raises:
            RuntimeError: if the callback has already been specified.
            RuntimeError: if import_files had already been specified.
        """

        if len(self._import_extension_callbacks) != 0:
            raise RuntimeError('import_files used, therefore cannot use import_directory')

        # The closure enforces arguments.
        def closure(dir_path: str,
                    context: Dict,
                    add_annotation: AnnotationFunction,
                    add_audio_file: AddAudioFunction):
            return f(dir_path, context, add_annotation, add_audio_file)
        # Store the closure by file extention
        if self._import_directory_callback is not None:
            raise RuntimeError('import_directory can only be used once')
        self._import_directory_callback = closure
        return closure

    def make_default_context(self, ctx: Dict):
        """
        Define a default context for the data transformer.

        :param ctx: dictionary of jsonable values.
        """
        self._default_context = json.dumps(ctx)
        return
    
    def audio_media_extention(self, extention: str):
        """
        Target media file type to process by file extention.

        :param extention: Extention part of file name.
        """
        self._audio_ext_filter = extention
        return

    def add_setting(self, figure, out, what, params):
        """"""
        pass

    def replace_reprocess_audio(self, f):
        """"""
        pass

    def export_files(self, f):
        """"""
        pass

    def export_directory(self, f):
        """"""
        pass

    def use_temporary_directory(self, f):
        """
        Python decotator.

        Postpends an argument containing the path to a temporary directory (before kwargs).

        :param f: function to be decorated.
        :return: Callable object containing the function.
        """
        
        functional = Functional(f)
        self._functions_using_tempdir.append(functional)

        return functional

    def build(self, collection_path: str, resampled_path: str, temporary_directory_path: str, transcription_json_file_path: str):
        """"""
        # Prepare a copy of the context object.
        context = json.loads(self._default_context)

        # Choose an importing methodology and prepare it. Options:
        #   _import_files
        #   _import_directory
        # Note: This function calls the audio processing callback
        importing_method = None


        def _import_directory(dt: DataTransformer, dir_path:str, context, add_annotation, add_audio):

            #
            # TODO: Extract audio and transcription data here
            #
            pass
            
        
        def _import_files(dt: DataTransformer, _, context, add_annotation, add_audio):
            extention_to_files: FilteredPathList = _filter_files_by_extention(collection_path)
            audio_paths: PathList = extention_to_files.pop(dt._audio_ext_filter)
            # process audio
            dt._audio_processing_callback(audio_paths, temporary_directory_path, resampled_path, add_audio)
            # process transcription data
            for extention, file_paths in extention_to_files.items():
                # only process the file type collection if a handler exists for it
                callback = self._import_extension_callbacks.get(extention, None)
                if callback is not None:
                    callback(file_paths, dt._context, add_annotation)
            
            # save transcription data to file
            with Path(transcription_json_file_path).open(mode='w') as fout:
                annotations = []
                for id in dt._annotation_store:
                    annotations.extend(dt._annotation_store[id])
                fout.write(json.dumps(annotations))
            return # _import_files


            
        if self._import_directory_callback is not None:
            importing_method = _import_directory
        else:
            importing_method = _import_files
        def _importing_closure(dt: DataTransformer, context: Dict):
            """
            A closure that prepares the call to the decided function, calls that function then saves the json result to file.
            """
            # Clean up from possible previous imports
            dt._annotation_store = {}
            dt._audio_store = {}

            # Callbacks to add data to the internal stores
            def add_annotation(id, obj):
                if id in dt._annotation_store:
                    dt._annotation_store[id].append(obj)
                else:
                    dt._annotation_store[id] = [obj]
                return # from add_annotation
            add_audio = lambda id, audio_path: dt._audio_store.update({id: audio_path})

            # Extract audio and transcription data here
            importing_method(dt, collection_path, context, add_annotation, add_audio)

            # save transcription data to file
            with Path(transcription_json_file_path).open(mode='w') as fout:
                annotations = []
                for id in dt._annotation_store:
                    annotations.extend(dt._annotation_store[id])
                fout.write(json.dumps(annotations))
            return # from process
        importing_function = _importing_closure
            

                

        # Prepare the audio function or use the replacement one
        audio_processing_callback = Functional(_default_audio_resampler)
        # register the default callback to have it's function restructured
        self._functions_using_tempdir.append(audio_processing_callback)

        # Note: the symbol dt is used in functions above it's definition, this
        # is intended as dt above is meant to be a pesudo-self argument which
        # will be the instance dt later.
        dt = DataTransformer(context, collection_path, resampled_path, temporary_directory_path, importing_function, audio_processing_callback)

        # restructure functions that require a temporary directory
        for functional in self._functions_using_tempdir:
            original_f = functional.callback
            def wrapper(*args, **kwargs):
                # Ensure the directory is empty
                path = Path(temporary_directory_path)
                if path.exists():
                    shutil.rmtree(temporary_directory_path)
                path.mkdir(parents=True)

                # run the function with the clean directory
                original_f(*args, temporary_directory_path, **kwargs)

                # delete the temporary directory
                shutil.rmtree(temporary_directory_path)
            functional.callback = wrapper

        return dt



def make_data_transformer(name: str, collection_path: str, resampled_path: str, temporary_directory_path: str, transcription_json_file_path: str) -> DataTransformer:
    """
    Creates a concrete data transformer.

    :param name: type of requested data transformer.
    :param collection_path: path to the original file collection.
    :param resampled_path: path to put resampled audio into.
    :param temporary_directory_path: path to store and operate on temporary data.
    :param transcription_json_file_path: path to save json file for transcription output data to.
    :returns: a DataTransformer of the requested type if it exists, else an error is raised.
    :raises:
        ValueError: if the requested data transformer does not exist.
    """
    

    dtaf: DataTransformerAbstractFactory = DataTransformerAbstractFactory._transformer_factories[name]
    dt = dtaf.build(collection_path, resampled_path, temporary_directory_path, transcription_json_file_path)
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

def _default_audio_resampler(self, audio_paths: List[str], resampled_dir_path: str, add_audio: AddAudioFunction, temp_dir_path: str):
    # TODO: Doc str, need temp_dir var at back of parameters list
    
    temp_dir_path = Path(temp_dir_path)
    resampled_dir_path = Path(resampled_dir_path)

    # Empty resampled contents
    if temp_dir_path.exists():
        shutil.rmtree(f'{temp_dir_path}')
    if resampled_dir_path.exists():
        shutil.rmtree(f'{resampled_dir_path}')
    temp_dir_path.mkdir(parents=True, exist_ok=True)
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

        # Clean up tmp folders
        for d in temporary_directories:
            os.rmdir(d)

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
