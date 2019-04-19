#!/usr/bin/python3

"""
Splits a directory of audio (.wav) files into short segments based on silence

Copyright: University of Queensland, 2019
Contributors:
              Nicholas Lambourne - (The University of Queensland, 2019)
"""

from argparse import ArgumentParser
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence
from kaldi_helpers.script_utilities import find_all_files_in_dir_by_extensions


def match_target_amplitude(segment: AudioSegment, target_dbfs) -> AudioSegment:
    """
    Matches an AudioSegment to a specified dBFS level.
    :param segment: AudioSegment to modify
    :param target_dbfs: integer repre
    :return: the segment matched to the target_dbfs
    """
    dbfs_delta = target_dbfs - segment.dBFS
    return segment.apply_gain(dbfs_delta)


def split_audio_file_on_silence(file_path: str,
                                output_directory: str,
                                min_silence_length: int,
                                threshold: int,
                                added_silence: int,
                                file_index: int) -> None:
    """
    Splits an AudioSegment into sub-segments based on silence detected by pydub.
    :param file_path: file path of the audio file to split
    :param output_directory: path to directory in which to write output files
    :param min_silence_length: the minimum length (in ms) of silence that indicates a break
    :param threshold: the level below the norm (in dBFS) to consider silence
    :param added_silence: silence to be added to the beginning and end of each split utterance
    :param file_index: the number of the file in the directory (recursive) to mark each sub-utterance with.
    """
    audio = AudioSegment(file_path)
    segments = split_on_silence(audio_segment=audio,
                                min_silence_len=min_silence_length,
                                silence_thresh=-threshold)
    silence = AudioSegment.silent(duration=added_silence)
    for segment_index, segment in enumerate(segments):
        audio_segment = silence + segment + silence
        normalised_segment = match_target_amplitude(audio_segment, -20)
        export_file_name = f"_file_{file_index}-part_{segment_index}.wav"
        print(f"Exporting {export_file_name}")
        normalised_segment.export(Path(output_directory, export_file_name))


def main() -> None:
    parser = ArgumentParser(description="Splits a directory of audio (.wav) files into short segments")
    parser.add_argument("-i", "--input_dir",
                        help="Directory containing audio to be split",
                        type=str,
                        required=True)
    parser.add_argument("-o", "--output_dir",
                        help="Directory to output the split audio",
                        type=str,
                        required=True)
    parser.add_argument("-s", "--silence_length",
                        help="Minimum length of silence in milliseconds",
                        type=int,
                        default=200)
    parser.add_argument("-t", "--threshold",
                        help="Threshold below norm to consider silence in dBFS (positive integer)",
                        type=int,
                        default=16)
    parser.add_argument("-a", "--added_silence",
                        help="Add silence to beginning and end of segments, in milliseconds",
                        type=int,
                        default=100)

    arguments = parser.parse_args()
    all_audio_files = find_all_files_in_dir_by_extensions(arguments.input_dir, {"wav"})

    for index, file_path in enumerate(all_audio_files):
        split_audio_file_on_silence(file_path=file_path,
                                    output_directory=arguments.output_dir,
                                    min_silence_length=arguments.silence_length,
                                    threshold=arguments.threshold,
                                    added_silence=arguments.added_silence,
                                    file_index=index)


if __name__ == "__main__":
    main()
