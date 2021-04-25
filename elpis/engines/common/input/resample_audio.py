#!/usr/bin/python3

"""
Converts audio to 16 bit 16k mono WAV

Copyright: University of Queensland, 2019
Contributors:
              Scott Heath - (The University of Queensland, 2017)
              Oliver Adams - (The University of Melbourne, 2018)
"""

import argparse
import glob
import os
import subprocess
import threading
from multiprocessing.dummy import Pool
from shutil import move
from typing import Set, Tuple

from ..utilities.globals import SOX_PATH


def join_norm(p1, p2) -> str:
    tmp = os.path.join(os.path.normpath(p1), os.path.normpath(p2))
    return os.path.normpath(tmp)


def process_item(sox_arguments: Tuple[int, str, threading.Lock, Set[str], str]) -> str:
    index, input_audio, lock, temporary_directories, parent_temporary_directory = sox_arguments

    input_name = os.path.normpath(input_audio)

    file_directory, file_name = os.path.split(input_audio)
    base_directory, ext = os.path.splitext(file_name)
    output_directory = os.path.join(file_directory, parent_temporary_directory)

    with lock:  # Avoids race condition
        temporary_directories.add(output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    temporary_file_name = join_norm(output_directory, "%s.%s" % (base_directory, "wav"))

    if not os.path.exists(temporary_file_name):
        sox_arguments = [SOX_PATH, input_name, "-b", "16", "-c", "1", "-r", "44.1k", "-t", "wav",
                         temporary_file_name]
        subprocess.call(sox_arguments)
    return temporary_file_name


def main() -> None:
    parser = argparse.ArgumentParser(description="This script will silence a wave file based on "
                                                 "annotations in an Elan tier ")
    parser.add_argument('-c', '--corpus',
                        help='Directory of audio and eaf files',
                        type=str,
                        default='../input/data')
    parser.add_argument('-o', '--overwrite',
                        help='Write over existing files',
                        action="store_true",
                        default=True)
    args = parser.parse_args()

    base_directory = args.corpus
    audio_extensions = {"*.wav"}
    parent_temporary_directory = "tmp"

    all_files_in_dir = glob.glob(os.path.join(base_directory, "**"), recursive=True)
    input_audio = [file_ for file_ in all_files_in_dir if file_.endswith(".wav")]
    process_lock = threading.Lock()
    temporary_directories = set()

    map_arguments = [(index, audio_path, process_lock, temporary_directories,
                      parent_temporary_directory)
                     for index, audio_path in enumerate(input_audio)]

    # Multi-Threaded Audio Re-sampling
    with Pool() as pool:
        outputs = pool.map(process_item, map_arguments)

        if args.overwrite:
            # Replace original files
            for audio_file in outputs:
                file_name = os.path.basename(audio_file)
                parent_directory = os.path.dirname(os.path.dirname(audio_file))
                move(audio_file, os.path.join(parent_directory, file_name))
            # Clean up tmp folders
            for d in temporary_directories:
                os.rmdir(d)


if __name__ == "__main__":
    main()
