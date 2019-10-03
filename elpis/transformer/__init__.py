import os
import importlib
import json
from typing import List, Dict, Callable
from pathlib import Path

# A json_str is the same as a normal string except must always be deserializable into JSON as an invariant.
json_str = str

AnnotationFunction = Callable[[Dict], None]
FileImporterType = Callable[[List[str], Dict, AnnotationFunction], None]
DirImporterType = Callable[[str, Dict, AnnotationFunction], None]
AddAudioFunction = Callable[[str, str], None]
AudioProcessingFunction = Callable[[List[str], Dict, AddAudioFunction], None]

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


class DataTransformer:
    """
    A data transformer handles the importing and exporting of data from the
    Elpis pipeline system.
    """

    def __init__(self, context: Dict, collection_path: str, resampled_path: str, temporary_directory_path: str, importing_function: DirImporterType, audio_processing_callback: AudioProcessingFunction):
        self._context: Dict = context

        # Path to directory containing original audio and transcription files
        self._collection_path: str = collection_path

        # Path to directory containing resampled audio files
        self._resampled_path: str = resampled_path

        # Path to a temporary directory for resampled files. Could be deleted
        # after running process().
        self._temporary_directory_path: str = temporary_directory_path

        # Callback to transcription data importing function, requires contents
        # directoru, contect and add_annotaion parameters.
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
        # Process audio first to create IDS.
        # Process transcription data structures.

        add_annotation = lambda id, obj: self._annotation_store[id].append(obj)
        self._importing_function(self, self._collection_path, self._context, add_annotation)




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

    def export_file(self, f):
        """"""
        pass

    def export_directory(self, f):
        """"""
        pass

    def build(self, collection_path: str, resampled_path: str, temporary_directory_path: str):
        """"""
        # Prepare a copy of the context object.
        context = json.loads(self._default_context)

        # Choose an importing methodology and prepare it.
        # Note: This function calls the audio
        importing_function = None
        def _import_files(dt: DataTransformer, dir_path, context, add_annotation):
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

                # process audio first to generate IDs
                for file_path in extention_to_files[self._audio_ext_filter]:
                    id = file_path.split('/')[-1][:-1-len(self._audio_ext_filter)]
                    dt._audio_store[id] = file_path###???
                    # prepare list of annotations per id
                    dt._annotation_store[id] = []
                


        def _import_directory(dt: DataTransformer, dir_path, context, add_annotation):
            pass
        if self._import_directory_callback is not None:
            importing_function = _import_directory
        else:
            importing_function = _import_files

        # Prepare the audio function or use the replacement one
        audio_processing_callback = None
        def default_audio_processing():
            pass

        # Note: the symbol dt is used in functions above it's definition, this
        # is intended as dt above is meant to be a pesudo-self argument which
        # will be the instance dt later.
        dt = DataTransformer(context, collection_path, resampled_path, temporary_directory_path, importing_function, audio_processing_callback)

        return dt



def make_data_transformer(name: str, collection_path: str, resampled_path: str, temporary_directory_path: str):
    """
    Creates a concrete data transformer.

    :param name: type of requested data transformer.
    :param collection_path: path to the original file collection.
    :param resampled_path: path to put resampled audio into.
    :param temporary_directory_path: path to store and operate on temporary data.
    :returns: a DataTransformer of the requested type if it exists, else an error is raised.
    :raises:
        ValueError: if the requested data transformer does not exist.
    """
    pass
    # ensure the data transformer factory does not already exist.

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
