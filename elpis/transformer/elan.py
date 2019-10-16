#!/usr/bin/python3

"""
Copyright: University of Queensland, 2019
Contributors:
              Josh Arnold - (The University of Queensland, 2017)
              Ben Foley - (The University of Queensland, 2018)
              Nicholas Lambourne - (The University of Queensland, 2019)
              Nicholas Buckeridge - (The University of Queensland, 2019)
"""

import re
import string
import sys
import os
import nltk
import codecs
from csv import reader
from pympi.Elan import Eaf
from langid.langid import LanguageIdentifier, model
from nltk.corpus import words
from praatio import tgio
from typing import Dict, List, Set, Tuple
from pathlib import Path

from elpis.transformer import DataTransformerAbstractFactory

elan = DataTransformerAbstractFactory('Elan')


elan.set_audio_extention('wav')

DEFAULT_TIER = 'Phrase'
GRAPHIC_RESOURCE_NAME = 'elan.png'

elan.set_default_context({
    'tier': DEFAULT_TIER,
    'graphic': GRAPHIC_RESOURCE_NAME
})

@elan.import_files('eaf')
def import_eaf_file(eaf_paths, context, add_annotation, tmp_dir):
    """
    Import handler for processing all .wav and .eaf files.

    :param wav_paths: List of string paths to Wave files.
    :param eaf_paths: List of string paths to Elan files.
    """

    """
    Import handler for processing all .eaf files.

    Method to process a particular tier in an eaf file (ELAN Annotation Format). It stores the transcriptions in the 
    following format:
                    {'speaker_id': <speaker_id>,
                    'audio_file_name': <file_name>,
                    'transcript': <transcription_label>,
                    'start_ms': <start_time_in_milliseconds>,
                    'stop_ms': <stop_time_in_milliseconds>}

    :param eaf_paths: List of string paths to Elan files.
    :return: a list of dictionaries, where each dictionary is an annotation
    """
    for input_elan_file in eaf_paths:
        # Get paths to files
        input_directory, full_file_name = os.path.split(input_elan_file)
        file_name, extension = os.path.splitext(full_file_name)

        input_eaf = Eaf(input_elan_file)

        # TODO: Check if this is necessary? It is possible to process transcription and audio file separately.
        # # Look for wav file matching the eaf file in same directory
        # if os.path.isfile(os.path.join(input_directory, file_name + ".wav")):
        #     print("WAV file found for " + file_name, file=sys.stderr)
        # else:
        #     raise ValueError(f"WAV file not found for {full_file_name}. "
        #                     f"Please put it next to the eaf file in {input_directory}.")

        # Get annotations and parameters (things like speaker id) on the target tier
        tier_name = context['tier']
        annotations = sorted(input_eaf.get_annotation_data_for_tier(tier_name))
        parameters = input_eaf.get_parameters_for_tier(tier_name)
        speaker_id = parameters.get("PARTICIPANT", "")

        annotations_data = []

        for annotation in annotations:
            start = annotation[0]
            end = annotation[1]
            annotation = annotation[2]

            # print("processing annotation: " + annotation, start, end)
            obj = {
                "audio_file_name": f"{file_name}.wav",
                "transcript": annotation,
                "start_ms": start,
                "stop_ms": end
            }
            # TODO: prehaps re-enable later
            # if "PARTICIPANT" in parameters:
            #     obj["speaker_id"] = speaker_id
            utterance = clean_json(obj)
            add_annotation(file_name, utterance)


# @elan.add_setting('textbox', label='Tier', default=DEFAULT_TIER)
# def change_tier(text, context):
#     context['tier'] = text


def get_english_words() -> Set[str]:
    """
    Gets a list of English words from the nltk corpora (~235k words).
    N.B: will download the word list if not already available (~740kB), requires internet.
    :return: a set containing the English words
    """
    nltk.download("words")  # Will only download if not locally available.
    return set(words.words())


def clean_utterance(utterance: Dict[str, str],
                    remove_english: bool = False,
                    english_words: set = None,
                    punctuation: str = None,
                    special_cases: List[str] = None) -> (List[str], int):
    """
    Takes an utterance and cleans it based on the rules established by the provided parameters.
    :param utterance: a dictionary with a "transcript" key-value pair.
    :param remove_english: whether or not to remove English dirty_words.
    :param english_words: a list of english dirty_words to remove from the transcript (we suggest the nltk dirty_words corpora).
    :param punctuation: list of punctuation symbols to remove from the transcript.
    :param special_cases: a list of dirty_words to always remove from the output.
    :return: a tuple with a list of 'cleaned' dirty_words and a number representing the number of English dirty_words to remove.
    """
    translation_tags = {"@eng@", "<ind:", "<eng:"}
    utterance_string = utterance.get("transcript").lower()
    dirty_words = utterance_string.split()
    clean_words = []
    english_word_count = 0
    for word in dirty_words:
        if special_cases and word in special_cases:
            continue
        if word in translation_tags:  # Translations / ignore
            return [], 0
        # If a word contains a digit, throw out whole utterance
        if bool(re.search(r"\d", word)) and not word.isdigit():
            return [], 0
        if punctuation:
            for mark in punctuation:
                word = word.replace(mark, "")
        if remove_english and len(word) > 3 and word in english_words:
            english_word_count += 1
            continue
        clean_words.append(word)
    return clean_words, english_word_count


def is_valid_utterance(clean_words: List[str],
                       english_word_count: int,
                       remove_english: bool,
                       use_langid: bool,
                       langid_identifier: LanguageIdentifier) -> bool:
    """
    Determines whether a cleaned utterance (list of words) is valid based on the provided parameters.
    :param clean_words: a list of clean word strings.
    :param english_word_count: the number of english words removed from the string during cleaning.
    :param remove_english: whether or not to remove english words.
    :param use_langid: whether or not to use the langid library to determine if a word is English.
    :param langid_identifier: language identifier object to use with langid library.
    :return: True if utterance is valid, false otherwise.
    """
    # Exclude utterance if empty after cleaning
    cleaned_transcription = " ".join(clean_words).strip()
    if cleaned_transcription == "":
        return False

    # Exclude utterance if > 10% english
    if remove_english and len(clean_words) > 0 and english_word_count / len(clean_words) > 0.1:
        # print(round(english_word_count / len(clean_words)), trans, file=sys.stderr)
        return False

    # Exclude utterance if langid thinks its english
    if remove_english and use_langid:
        lang, prob = langid_identifier.classify(cleaned_transcription)
        if lang == "en" and prob > 0.5:
            return False
    return True


def clean_json(utterance: Dict[str, str],
                    remove_english: bool = False,
                    use_langid: bool = False) -> Dict[str, str]:
    """
    Clean a utterances (Python dictionaries) based on the given parameters.
    :param utterance: a 'transcription' key-value utterance.
    :param remove_english: whether or not to remove English from the utterances.
    :param use_langid: whether or not to use the langid library to identify English to remove.
    :return: cleaned utterances.
    """
    punctuation_to_remove = string.punctuation + "…’“–”‘°"
    special_cases = ["<silence>"]  # Any words you want to ignore
    langid_identifier = None

    if remove_english:
        english_words = get_english_words()  # pre-load English corpus
        if use_langid:
            langid_identifier = LanguageIdentifier.from_modelstring(model,
                                                                    norm_probs=True)
    else:
        english_words = set()

    clean_words, english_word_count = clean_utterance(utterance=utterance,
                                                        remove_english=remove_english,
                                                        english_words=english_words,
                                                        punctuation=punctuation_to_remove,
                                                        special_cases=special_cases)

    if is_valid_utterance(clean_words,
                            english_word_count,
                            remove_english,
                            use_langid,
                            langid_identifier):
        cleaned_transcript = " ".join(clean_words).strip()
        utterance["transcript"] = cleaned_transcript

    return utterance

def ctm_to_dictionary(ctm_file_path: str,
                      segments_dictionary: Dict[str, str]) -> dict:
    with codecs.open(ctm_file_path, encoding="utf8") as file:
        ctm_entries = list(reader(file, delimiter=" "))
    textgrid_dictionary = dict()
    for entry in ctm_entries:
        utterance_id, segment_start_time = segments_dictionary[entry[0]]
        if utterance_id not in textgrid_dictionary:
            textgrid_dictionary[utterance_id] = []
        relative_start_time = float(entry[2])
        absolute_start_time = segment_start_time + relative_start_time
        absolute_end_time = absolute_start_time + float(entry[3])
        inferred_text = entry[4]
        utterance_segment = (str(absolute_start_time),
                             str(absolute_end_time),
                             inferred_text)
        textgrid_dictionary[utterance_id].append(utterance_segment)
    return textgrid_dictionary


def get_segment_dictionary(segment_file_name: str) -> Dict[str, Tuple[str, float]]:
    with open(segment_file_name, "r") as file:
        segment_entries = list(reader(file, delimiter=" "))
    segment_dictionary = dict()
    for entry in segment_entries:
        segment_id = entry[0]
        utterance_id = entry[1]
        start_time = float(entry[2])
        segment_dictionary[segment_id] = (utterance_id, start_time)
    return segment_dictionary


def wav_scp_to_dictionary(scp_file_name: str) -> dict:
    wav_dictionary = dict()
    with open(scp_file_name) as file:
        wav_entries = list(reader(file, delimiter=" "))
        for entry in wav_entries:
            utterance_id = entry[0]
            wav_file_path = entry[1]
            wav_dictionary[utterance_id] = wav_file_path
    return wav_dictionary


def create_textgrid(wav_dictionary: Dict[str, str],
                    ctm_dictionary: dict,
                    output_directory: str) -> None:
    for index, utterance_id in enumerate(wav_dictionary.keys()):
        textgrid = tgio.Textgrid()
        tier = tgio.IntervalTier(name='phones',
                                 entryList=ctm_dictionary[utterance_id],
                                 minT=0,
                                 pairedWav=str(Path(wav_dictionary[utterance_id])))
        textgrid.addTier(tier)
        textgrid.save(str(Path(output_directory, f"utterance-{index}.TextGrid")))