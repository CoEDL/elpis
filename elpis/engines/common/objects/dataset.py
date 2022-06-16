import json
import glob
from loguru import logger
import os
import string

from pathlib import Path
from typing import Dict, List, Union, BinaryIO, Optional
from io import BufferedIOBase

from ..utilities import load_json_file
from elpis.transformer import (
    make_importer,
    DataTransformer,
    DataTransformerAbstractFactory,
)
from elpis.engines.common.objects.fsobject import FSObject
from elpis.engines.common.objects.path_structure import (
    existing_attributes,
    ensure_paths_exist,
)
from elpis.engines.common.input.clean_json import extract_additional_corpora
from elpis.engines.common.input.make_wordlist import generate_word_list


class DSPaths(object):
    """
    Path locations for the DataSet object. Attributes represent paths to DataSet artifacts.
    """

    def __init__(self, basepath: Path):
        # directories
        attrs = existing_attributes(self)
        self.basepath = basepath
        self.original = self.basepath.joinpath("original")
        self.cleaned = self.basepath.joinpath("cleaned")
        self.resampled = self.basepath.joinpath("resampled")
        self.text_corpora = self.original.joinpath("text_corpora")
        ensure_paths_exist(self, attrs)

        # files
        self.annotation_json: Path = self.basepath.joinpath("annotations.json")
        self.word_count_json: Path = self.basepath.joinpath("word_count.json")
        self.word_list_txt: Path = self.basepath.joinpath("word_list.txt")
        # \/ user uploaded addional words
        self.additional_word_list_txt = self.original.joinpath(
            "additional_word_list.txt"
        )
        # \/ compile the uploaded corpora into this single file
        self.corpus_txt = self.cleaned.joinpath("corpus.txt")


class Dataset(FSObject):
    """
    Dataset (or commonly referred to as Recordings on the front end) stores
    the original and resampled audio, and original transcription files.
    Datasets in the same KaldiInterface must have unique names.
    """

    # The configuration settings stored in the file below.
    _config_file = "dataset.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__files: List[Path] = []
        self.pathto = DSPaths(self.path)
        self._importer = None

        # config
        self.config["has_been_processed"] = False
        self.config["files"] = []
        self.config["processed_labels"] = []
        self.config["importer"] = None

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.pathto = DSPaths(self.path)
        self.__files = [
            self.pathto.original.joinpath(path) for path in self.config["files"]
        ]
        # at this point config has the previous state
        self._importer = self.config["importer"]
        temp_state = self._importer
        # rebuild the importer, this resets importer ui
        if self._importer is not None:
            importer_name = self._importer["name"]
            self.select_importer(importer_name)
        # importer has been reset, copy the old state back
        self.config["importer"] = temp_state
        return self

    def select_importer(self, name: str):
        """
        Selects data transformer to use as importer corrosponding to the name.
        If no name exists, ValueError is raised. After this function is called,
        the .importer property is no longer None. If this function is called
        again, then the importer will be overriden.

        TODO context change callback

        :param name: name of the data transformer to use.
        :raises:
            ValueError: if name does not corrospond to any existing data transformers.
        """

        def settings_change_callback(ctx):
            """
            Generate the JSON importer (data transformer) state variable.
            """
            nonlocal name
            # TODO: is this function required?
            return

        # getters and setters for the subconfig for importers.
        def get_config_callback():
            return self.config["importer"]

        def set_config_callback(importer_config):
            self.config["importer"] = importer_config

        temporary_directory_path = f"/tmp/{self.hash}/working"
        Path(temporary_directory_path).mkdir(
            parents=True, exist_ok=True
        )  # TODO: what if two importers are used on this directory?
        transcription_json_file_path = f"{self.pathto.annotation_json}"
        self._importer = make_importer(
            name,
            str(self.pathto.original),
            str(self.pathto.resampled),
            temporary_directory_path,
            transcription_json_file_path,
            get_config_callback,
            set_config_callback,
            settings_change_callback=settings_change_callback,
        )
        return

    def auto_select_importer(self):
        if self.importer is not None:
            return  # Already have importer selected
        if len(self.files) == 0:
            return  # cannot determine importer with no files.
        extensions = set([f"{p}".split(".")[-1] for p in self.files])
        dtaf_exts = set(DataTransformerAbstractFactory._ext_to_factory.keys())
        intersect = extensions.intersection(dtaf_exts)
        if len(intersect) == 0:
            return  # No common file extentions
        # Just use the first one
        ext = list(intersect)[0]
        name = DataTransformerAbstractFactory._ext_to_factory[ext]
        self.select_importer(name)

    @property
    def files(self) -> List[str]:
        """
        Gives list of currently held files.

        As a property, this attribute is read-only.

        :returns: a list of file paths internal to this structure.
        """
        return self.config["files"]

    @property
    def has_been_processed(self) -> bool:
        """
        Boolean flag that is true if the process function has been run and the
        dataset has not been chaged since. The dataset is considered changed
        if the file list is manipulated (added to or have items removed).

        As a property, this attribute is read-only.

        :return: True if the process function has been run and the
        dataset has not been chaged since, otherwise false.
        """
        return self.config["has_been_processed"]

    @property
    def processed_labels(self) -> List[str]:
        """
        Provide a list of the labels that have been processed. The list by
        default is empty until files are added to the dataset and the process()
        function is run. Labels are added by the data transformer used. If
        after the process function is run and the dataset file list is
        modified, then the dataset is considered unprocessed and the labels
        list will return to their default empty list state.

        As a property, this attribute is read-only.

        :return: List of processed labels by the data transformer.
        """
        return self.config["processed_labels"]

    @property
    def importer(self) -> DataTransformer:
        """
        Access the data transformer assigned to this dataset.

        As a property, this attribute is read-only, however, can be operated on.

        :return: A DataTransformer if one has been assigned using the select_importer(...) method, otherwise None.
        """
        return self._importer

    @property
    def annotations(self) -> dict:
        """
        Returns the contents of the annotaions.json object. This is the file
        where the data transformer puts processed annotations.

        As a property, this attribute is read-only.

        :return: the annotations json object.
        :raises:
            RuntimeError: if there is an attempt to get the annotation object before process().
        """
        if self.config["has_been_processed"] == False:
            raise RuntimeError("cannot get annotations wihtout runnint .process()")
        with self.pathto.annotation_json.open(mode="r") as fin:
            return json.loads(fin.read())

    def add_fp(
        self,
        fp: Union[BufferedIOBase, BinaryIO],
        fname: str,
        destination: str = "original",
    ):
        """
        Saves a copy of the file pointer contents in the internal datastructure
        at `self.pathto.original`. This method enforces a copy to be made and
        ensures the original files remain untouched. All file adding methods
        such as add_file and add_directory use this to add individual files.

        :param fp: Python file BufferedIOBase object usually from open().
        :param fname: name of the file.
        """

        # TODO
        # change this after adding a seperate file upload widget in gui for additional corpora files
        # then we can determine where to write the files by destination value instead of by name
        if "corpus" in fname:
            path: Path = self.pathto.text_corpora.joinpath(fname)
        else:
            path: Path = self.pathto.original.joinpath(fname)
        with path.open(mode="wb") as fout:
            fout.write(fp.read())

        if fname not in self.config["files"]:
            self.__files.append(path)
            self.config["files"] = [f"{f.name}" for f in self.__files]
        else:
            # already existed but has been overriden, name is already in the config
            pass

    def add_file(self, file_path: str):
        """
        Copies the file at the given path into the internal data structure.

        When this action happens, the internal file state is changed and the
        dataset is marked as unprocessed (has_been_processed == False).

        :param file_path: is the string path to the file to be added.
        :raises:
            - ValueError: if the file cannot be openned.
        """
        file_path = Path(file_path)
        if not file_path.is_file():
            raise ValueError(f'"{file_path}" is not a valid path to file"')
        with file_path.open(mode="rb") as fin:
            self.add_fp(fin, file_path.name)
        self.config["has_been_processed"] = False
        self.config["processed_labels"] = []

    def add_directory(self, path, extensions: Optional[List[str]] = None):
        """
        Add all the contents of the given directory to the dataset.

        When this action happens, the internal file state is changed and the
        dataset is marked as unprocessed (has_been_processed == False).

        :param path: is the string path to the directory containing the files to be added.
        :param extensions: Optional keyword parameter, if set must be a list of file extentions to
        filter files in the directory.
        :raises:
            - ValueError: if the file cannot be openned.
        """
        extensions = extensions or list()
        path: Path = Path(path)
        for filepath in path.iterdir():
            if len(extensions) != 0:
                if filepath.name.split(".")[-1] not in extensions:
                    continue
            file_pointer = filepath.open(mode="rb")
            self.add_fp(file_pointer, filepath.name)
        self.config["has_been_processed"] = False
        self.config["processed_labels"] = []

    def remove_file(self, file_name: str):
        """
        Removes a file from the file set. The file name must exist (that is it
        must be listed in .files) otherwise an error is raised.

        When this action happens, the internal file state is changed and the
        dataset is marked as unprocessed (has_been_processed == False).

        :param file_name: is the name of the file to remove from the internal set.
        :raises:
            - ValueError: if the file name is not in the internal set.
        """
        # Search for file then delete it.
        file_path: Optional[Path] = None
        for path in self.__files:
            if path.name == file_name:
                file_path = path
                break
        if file_path is None:
            raise ValueError(f'file named "{file_name}" is not the internal set')
        self.__files.remove(file_path)
        file_path.unlink()  # Deletes the file.
        self.config["files"] = [f"{f.name}" for f in self.__files]
        self.config["has_been_processed"] = False
        self.config["processed_labels"] = []

    @property
    def state(self):
        """
        An API fiendly state representation of the object.

        Invarient: The returned object can be converted to JSON using json.load(...).

        :returns: the objects state.
        """
        _config = self.config._load()
        return {
            "name": self.config["name"],
            "hash": self.config["hash"],
            "date": self.config["date"],
            "has_been_processed": self.config["has_been_processed"],
            "files": self.config["files"],
            "processed_labels": self.config["processed_labels"],
            "importer": self.config["importer"],
        }

    def validate(self):
        extention_to_path = {}
        for path in self.__files:
            extention = f"{path}".split(".")[-1]
            if extention not in extention_to_path.keys():
                extention_to_path[extention] = [path]
            else:
                extention_to_path[extention].append(path)
        for extention, paths in extention_to_path.items():
            self.importer.validate_files(extention, paths)

    def refresh_ui(self):
        self.importer.refresh_ui(self.__files)

    def process(self):
        transformer = self._importer
        if transformer == None:
            raise RuntimeError("must select importer before processing")
        transformer.process()
        settings = transformer.get_settings()
        # Compile text corpora from original/text_corpora dir into one file
        all_files_in_dir = set(
            glob.glob(os.path.join(str(self.pathto.text_corpora), "**"), recursive=True)
        )
        corpus_files = []
        for file_ in all_files_in_dir:
            file_name, extension = os.path.splitext(file_)
            if extension == ".txt":
                corpus_files.append(file_)
        logger.info(f"corpus_files {corpus_files}")
        # Compile and clean the additional corpora content into a single file
        # Reset first to prevent files being added multiple times
        if os.path.exists(self.pathto.corpus_txt):
            self.pathto.corpus_txt.unlink()
        for additional_corpus in corpus_files:
            extract_additional_corpora(
                additional_corpus=additional_corpus,
                corpus_txt=f"{self.pathto.corpus_txt}",
                punctuation_to_collapse_by=settings["punctuation_to_collapse_by"],
                punctuation_to_explode_by=settings["punctuation_to_explode_by"],
            )
        # task make-wordlist
        generate_word_list(
            transcription_file=f"{self.pathto.annotation_json}",
            output_file=f"{self.pathto.word_list_txt}",
            additional_word_list_file=f"{self.pathto.additional_word_list_txt}",
            additional_corpus_txt=f"{self.pathto.corpus_txt}",
        )
        # make word count
        annotations: List[Dict[str, str]] = load_json_file(
            f"{self.pathto.annotation_json}"
        )
        with self.pathto.word_count_json.open(mode="w") as f_word_count:
            wordlist = {}
            for transcription in annotations:
                words = transcription["transcript"].split()
                for word in words:
                    if word in wordlist:
                        wordlist[word] += 1
                    else:
                        wordlist[word] = 1
            json.dump(wordlist, f_word_count)

        self.config["has_been_processed"] = True

        annotation_labels_set = set(self._importer._annotation_store.keys())
        audio_labels_set = set(self._importer._audio_store.keys())
        processed_labels = annotation_labels_set.intersection(audio_labels_set)
        self.config["processed_labels"] = list(processed_labels)
