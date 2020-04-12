import json
import shutil
import glob
import os
import threading
import string

from pathlib import Path
from typing import List, Union, BinaryIO, Set
from io import BufferedIOBase
from multiprocessing.dummy import Pool
from shutil import move
from pympi.Elan import Eaf

from .fsobject import FSObject
from elpis.wrappers.objects.path_structure import existing_attributes, ensure_paths_exist

from elpis.wrappers.input.elan_to_json import process_eaf
from elpis.wrappers.input.clean_json import clean_json_data, extract_additional_corpora
from elpis.wrappers.input.resample_audio import process_item
from elpis.wrappers.input.make_wordlist import generate_word_list


# TODO: this is very ELAN specific code...
DEFAULT_TIER_TYPE = 'default-lt'
DEFAULT_TIER_NAME = 'Phrase'


class DSPaths(object):
    """
    Path locations for the DataSet object. Attribures represent paths to DataSet artifacts.
    """
    def __init__(self, basepath: Path):
        # directories
        attrs = existing_attributes(self)
        self.basepath = basepath
        self.original = self.basepath.joinpath('original')
        self.cleaned = self.basepath.joinpath('cleaned')
        self.resampled = self.basepath.joinpath('resampled')
        self.text_corpora = self.original.joinpath('text_corpora')
        ensure_paths_exist(self, attrs)

        # files
        self.corpus_tiers: Path = self.basepath.joinpath('corpus_tiers.json')
        self.filtered_json: Path = self.basepath.joinpath('filtered.json')
        self.word_count_json: Path = self.basepath.joinpath('word_count.json')
        self.word_list_txt: Path = self.basepath.joinpath('word_list.txt')
        # \/ user uploaded addional words
        self.additional_word_list_txt = self.original.joinpath('additional_word_list.txt')
        # \/ compile the uploaded corpora into this single file
        self.corpus_txt = self.cleaned.joinpath('corpus.txt')


class Dataset(FSObject):
    """
    Dataset (or commonly referred to as Recordings on the front end) stores
    the original and resampled audio, and original transcription files.
    Datasets in the same KaldiInterface must have unique names.
    """

    # The configuration settings stored in the file below.
    _config_file = 'dataset.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__files: List[Path] = []
        self.pathto = DSPaths(self.path)
        self.has_been_processed = False

        # config
        self.config['has_been_processed'] = False
        self.config['files'] = []
        # It's OK to have chars in the collapse list that are also in the explode list
        # because explode will be done first, removing them from the text,
        # thus they won't match during the collapse step
        self.config['punctuation_to_collapse_by'] = string.punctuation + ",…‘’“”°"
        self.config['punctuation_to_explode_by'] = "-"

        # All tier types and names for entire dataset
        # This is also very Elan-specific!
        self.config['tier_max_count'] = 1
        self.config['tier_types'] = []
        self.config['tier_names'] = []
        self.config['tier_order'] = 1
        self.config['tier_type'] = ""
        self.config['tier_name'] = ""

    @classmethod
    def load(cls, base_path: Path):
        self = super().load(base_path)
        self.__files = [Path(path) for path in self.config['files']]
        self.pathto = DSPaths(self.path)
        self.has_been_processed = self.config['has_been_processed']
        return self

    @property
    def files(self):
        return self.config['files']

    @property
    def tier_max_count(self) -> int:
        return self.config['tier_max_count']

    @tier_max_count.setter
    def tier_max_count(self, value: int):
        self.config['tier_max_count'] = value

    @property
    def tier_order(self) -> int:
        return self.config['tier_order']

    @tier_order.setter
    def tier_order(self, value: int):
        self.config['tier_order'] = value

    @property
    def tier_types(self) -> List[str]:
        return self.config['tier_types']

    @tier_types.setter
    def tier_types(self, value: List[str]):
        self.config['tier_types'] = value

    @property
    def tier_type(self) -> str:
        return self.config['tier_type']

    @tier_type.setter
    def tier_type(self, value: str):
        self.config['tier_type'] = value

    @property
    def tier_names(self) -> List[str]:
        return self.config['tier_names']

    @tier_names.setter
    def tier_names(self, value: List[str]):
        self.config['tier_names'] = value

    @property
    def tier_name(self) -> str:
        return self.config['tier_name']

    @tier_name.setter
    def tier_name(self, value: str):
        self.config['tier_name'] = value


    def get_elan_tier_attributes(self, input_dir: Path = Path('.')):
        """
        Iterate a dir of elan files and compiles info about all the files' tiers:
        unique tier types, unique tier names, and the num of tiers
        """
        # Use sets internally for easy uniqueness, conver to lists when done
        _tier_types: Set[str] = set()
        _tier_names: Set[str] = set()
        all_files_in_directory: Set[str] = set(
            glob.glob(os.path.join(input_dir, "**"), recursive=True))
        input_eafs_files: List[str] = [
            file_ for file_ in all_files_in_directory if file_.endswith(".eaf")]
        for file_ in input_eafs_files:
            input_eaf = Eaf(file_)
            for tier_type in list(input_eaf.get_linguistic_type_names()):
                _tier_types.add(tier_type)
                tier_ids: List[str] = input_eaf.get_tier_ids_for_linguistic_type(
                    tier_type)
                for tier_id in tier_ids:
                    _tier_names.add(tier_id)
            # count the number of tiers, use the max from all files
            tier_count = len(list(input_eaf.get_tier_names()))
            if tier_count > self.tier_max_count:
                self.tier_max_count = tier_count
        self.tier_types = list(_tier_types)
        self.tier_names = list(_tier_names)


    def add_elan_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return []

    def add_textgrid_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return []

    def add_transcriber_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return []

    def add_wave_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return []

    def add_other_audio_type_file(self, filename, content) -> None:
        # TODO: unimplemented!
        return []

    def list_audio_files(self) -> List[str]:
        # TODO: unimplemented!
        return []

    def list_transcription_files(self) -> List[str]:
        # TODO: unimplemented!
        return []

    def list_all_files(self) -> List[str]:
        # TODO: unimplemented!
        return []

    def remove_file(self, filename) -> None:
        # TODO: unimplemented!
        return

    def add_fp(self, fp: Union[BufferedIOBase, BinaryIO],
               fname: str,
               destination: str = 'original'):
        # TODO
        # change this after adding a seperate file upload widget in gui for additional corpora files
        # then we can determine where to write the files by destination value instead of by name
        if "corpus" in fname:
            path: Path = self.pathto.text_corpora.joinpath(fname)
        else:
            path: Path = self.pathto.original.joinpath(fname)

        with path.open(mode='wb') as fout:
            fout.write(fp.read())
        self.__files.append(path)
        self.config['files'] = [f'{f.name}' for f in self.__files]

    def add_directory(self, path, filter_=None):
        if not filter_:
            filter_ = []
        """Add all the contents of the given directory to the dataset."""
        path: Path = Path(path)
        for filepath in path.iterdir():
            if len(filter_) != 0:
                if filepath.name.split('.')[-1] not in filter_:
                    continue
            file_pointer = filepath.open(mode='rb')
            self.add_fp(fp=file_pointer, fname=filepath.name)

    def process(self):
        # remove existing file in resampled
        # TODO check what other files need removing
        shutil.rmtree(f'{self.pathto.resampled}')
        self.pathto.resampled.mkdir(parents=True, exist_ok=True)
        # Reset the target corpus file so re-processing doesn't append
        open(self.pathto.corpus_txt, 'w').close()
        # Reset the corpus tier metadata file
        open(self.pathto.corpus_tiers, 'w').close()

        # process files
        dirty = []
        for file in self.__files:
            if file.name.endswith('.eaf'):
                obj = process_eaf(input_elan_file=f'{self.pathto.original.joinpath(file)}',
                                  tier_order=self.tier_order,
                                  tier_type=self.tier_type,
                                  tier_name=self.tier_name,
                                  corpus_tiers_file=f'{self.pathto.corpus_tiers}')
                dirty.extend(obj)
        # TODO other options for command below: remove_english=arguments.remove_eng, use_langid=arguments.use_lang_id
        # Clean punctuation
        filtered = clean_json_data(json_data=dirty,
                                   punctuation_to_collapse_by=self.config['punctuation_to_collapse_by'],
                                   punctuation_to_explode_by=self.config['punctuation_to_explode_by'])
        with self.pathto.filtered_json.open(mode='w') as fout:
            json.dump(filtered, fout)
            # Write a file with word counts for just the transcription content
            with self.pathto.word_count_json.open(mode='w') as f_word_count:
                wordlist = {}
                for transcription in filtered:
                    words = transcription['transcript'].split()
                    for word in words:
                        if word in wordlist:
                            wordlist[word] += 1
                        else:
                            wordlist[word] = 1
                json.dump(wordlist, f_word_count)

        base_directory = f'{self.pathto.original}'
        temporary_directory_path = Path(f'/tmp/{self.hash}/working')
        temporary_directory_path.mkdir(parents=True, exist_ok=True)
        temporary_directory = f'{temporary_directory_path}'

        all_files_in_dir = glob.glob(os.path.join(
            base_directory, "**"), recursive=True)
        input_audio = [
            file_ for file_ in all_files_in_dir if file_.endswith(".wav")]
        process_lock = threading.Lock()
        temporary_directories = set()

        map_arguments = [(index, audio_path, process_lock, temporary_directories, temporary_directory)
                         for index, audio_path in enumerate(input_audio)]
        # Multi-Threaded Audio Re-sampling
        with Pool() as pool:
            outputs = pool.map(process_item, map_arguments)
            # TODO: overwrite?
            # Replace original files
            for audio_file in outputs:
                move(audio_file, self.pathto.resampled)
                # file_name = os.path.basename(audio_file)
                # parent_directory = os.path.dirname(os.path.dirname(audio_file))
                # move(audio_file, os.path.join(parent_directory, file_name))
            # Clean up tmp folders
            for d in temporary_directories:
                os.rmdir(d)

        # Compile text corpora from original/text_corpora dir into one file
        all_files_in_dir = set(glob.glob(os.path.join(
            self.pathto.text_corpora, "**"), recursive=True))
        corpus_files = []
        for file_ in all_files_in_dir:
            file_name, extension = os.path.splitext(file_)
            if extension == ".txt":
                corpus_files.append(file_)
        print(f"corpus_files {corpus_files}")
        # Compile and clean the additional corpora content into a single file
        for additional_corpus in corpus_files:
            extract_additional_corpora(additional_corpus=additional_corpus,
                                       corpus_txt=f'{self.pathto.corpus_txt}',
                                       punctuation_to_collapse_by=self.config['punctuation_to_collapse_by'],
                                       punctuation_to_explode_by=self.config['punctuation_to_explode_by'])

        # task make-wordlist
        generate_word_list(transcription_file=f'{self.pathto.filtered_json}',
                           output_file=f'{self.pathto.word_list_txt}',
                           additional_word_list_file=f'{self.pathto.additional_word_list_txt}',
                           additional_corpus_txt=f'{self.pathto.corpus_txt}'
                           )
        self.config['has_been_processed'] = True
