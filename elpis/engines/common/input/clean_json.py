#!/usr/bin/python3

"""
Given a json file with transcript information these tools can perform
- manipulations including generating word lists or filtering output to
- exclude english/punctuation.
- Optionally provide the output json file name with -j

Usage: python3 clean_json.py [-h] [--i INFILE] [--o OUTFILE] [-r] [-u]

Copyright: University of Queensland, 2019
Contributors:
              Josh Arnold - (The University of Queensland, 2017)
              Ben Foley - (The University of Queensland, 2018)
              Nicholas Lambourne - (The University of Queensland, 2019)
"""

import os
import re
import sys
import nltk
from argparse import ArgumentParser
from langid.langid import LanguageIdentifier, model
from nltk.corpus import words
from typing import Dict, List, Set
from ..utilities import load_json_file, write_data_to_json_file


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
                    punctuation_to_collapse_by: str = '',
                    punctuation_to_explode_by: str = '',
                    special_cases: List[str] = None) -> (List[str], int):
    """
    Takes an utterance and cleans it based on the rules established by the provided parameters.
    :param utterance: a dictionary with a "transcript" key-value pair.
    :param remove_english: whether or not to remove English dirty_words.
    :param punctuation_to_collapse_by: punctuation marks to strip
    :param punctuation_to_explode_by: punctuation marks to replace with spaces
    :param special_cases: a list of dirty_words to always remove from the output.
    :return: a tuple with a list of 'cleaned' words and a number representing the number of
             English dirty_words to remove.
    """
    print("*** clean_utterance")
    # TODO add interface setting to include user specific tags
    translation_tags = {"@eng@", "<ind:", "<eng:"}
    # TODO add interface setting to skip this as caps are significant in some languages
    utterance_string = utterance.get("transcript").lower()
    dirty_words = utterance_string.split()
    clean_words = []
    english_word_count = 0
    if remove_english:
        english_words = get_english_words()  # pre-load English corpus
    else:
        english_words = set()
    for word in dirty_words:
        if special_cases and word in special_cases:
            continue
        if word in translation_tags:  # Translations / ignore
            return [], 0
        word = deal_with_punctuation(text=word,
                                     punctuation_to_collapse_by=punctuation_to_collapse_by,
                                     punctuation_to_explode_by=punctuation_to_explode_by)
        if remove_english and len(word) > 3 and word in english_words:
            english_word_count += 1
            continue
        clean_words.append(word)
    return clean_words, english_word_count


def are_words_valid(clean_words: List[str],
                    english_word_count: int,
                    remove_english: bool,
                    use_langid: bool) -> bool:
    """
    Determines whether a list of words is valid based on the provided parameters.
    :param clean_words: a list of clean word strings.
    :param english_word_count: the number of english words removed from the string during cleaning.
    :param remove_english: whether or not to remove english words.
    :param use_langid: whether or not to use the langid library to determine if a word is English.
    :return: True if utterance is valid, False otherwise.
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
        langid_identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        lang, prob = langid_identifier.classify(cleaned_transcription)
        if lang == "en" and prob > 0.5:
            return False
    return True


def clean_json_utterance(utterance: Dict[str, str],
                         remove_english: bool = False,
                         use_langid: bool = False,
                         punctuation_to_collapse_by: str = '',
                         punctuation_to_explode_by: str = '') -> Dict[str, str]:
    """
    Clean an utterance (Python dictionary) based on the given parameters.
    :param utterance: Python dictionary, must have a 'transcript' key-value.
    :param remove_english: whether or not to remove English from the utterances.
    :param use_langid: whether or not to use the langid library to identify English to remove.
    :param punctuation_to_collapse_by: punctuation marks to strip
    :param punctuation_to_explode_by: punctuation marks to replace with spaces
    :return: cleaned utterances (dictionary).
    """

    # TODO make this an interface setting
    special_cases = ["<silence>"]  # Any words you want to ignore

    # Clean the text in the dict, returns a list of cleaned words
    clean_words, english_word_count = \
        clean_utterance(utterance=utterance,
                        remove_english=remove_english,
                        punctuation_to_collapse_by=punctuation_to_collapse_by,
                        punctuation_to_explode_by=punctuation_to_explode_by,
                        special_cases=special_cases)

    # Check that the cleaned words are valid (ie, not null, not English etc)
    if are_words_valid(clean_words,
                       english_word_count,
                       remove_english,
                       use_langid):
        cleaned_transcript = " ".join(clean_words).strip()
    else:
        # TODO is it best to return an empty str here or raise an error?
        cleaned_transcript = ""

    utterance['transcript'] = cleaned_transcript
    return utterance


def clean_json_data(json_data: List[Dict[str, str]],
                    remove_english: bool = False,
                    use_langid: bool = False,
                    punctuation_to_collapse_by: str = '',
                    punctuation_to_explode_by: str = '') -> List[Dict[str, str]]:
    """
    Clean a list of utterances (Python dictionaries) based on the given parameters.
    :param json_data: List of Python dictionaries, each must have a 'transcript' key-value.
    :param remove_english: whether or not to remove English from the utterances.
    :param use_langid: whether or not to use the langid library to identify English to remove.
    :param punctuation_to_collapse_by: punctuation marks to strip
    :param punctuation_to_explode_by: punctuation marks to replace with spaces
    :return: list of cleaned utterances (dictionaries).
    """
    json_data_cleaned = []
    for utterance in json_data:
        utterance_cleaned = clean_json_utterance(utterance,
                                                 remove_english=remove_english,
                                                 use_langid=use_langid,
                                                 punctuation_to_collapse_by=punctuation_to_collapse_by,
                                                 punctuation_to_explode_by=punctuation_to_explode_by)
        json_data_cleaned.append(utterance_cleaned)
    return json_data_cleaned


def extract_additional_corpora(additional_corpus: str = '',
                               corpus_txt: str = '',
                               punctuation_to_collapse_by: str = '',
                               punctuation_to_explode_by: str = '') -> None:
    """
    Takes a text file, extracts all sentences and writes them to the main corpus file.
    :param additional_corpus: the path to a plaintext file to extract additional sentences/lines from
    :param corpus_txt: the path to the compiled corpus.txt file
    :param punctuation_to_collapse_by: punctuation marks to strip
    :param punctuation_to_explode_by: punctuation marks to replace with spaces
    """
    print("corpus_txt", corpus_txt)
    if os.path.exists(corpus_txt):
        write_mode = 'a'  # append if already exists
    else:
        write_mode = 'w'  # make a new file if not
    with open(corpus_txt, write_mode) as corpus_txt_file:
        if os.path.exists(additional_corpus):
            print(f"Extracting corpus examples from: {additional_corpus}")
            with open(additional_corpus, "r", encoding="utf-8", ) as file_:
                for line in file_.readlines():
                    # clean the text along the way
                    line = \
                        deal_with_punctuation(text=line,
                                              punctuation_to_collapse_by=punctuation_to_collapse_by,
                                              punctuation_to_explode_by=punctuation_to_explode_by)
                    corpus_txt_file.writelines(line)
        else:
            print(f"Provided additional text additional_corpus file path invalid: "
                  f"{additional_corpus}")


def deal_with_punctuation(text: str = '',
                          punctuation_to_collapse_by: str = '',
                          punctuation_to_explode_by: str = '') -> str:
    """
    Removes punctuation from a string
    :param text: original text
    :param punctuation_to_collapse_by: punctuation marks to strip
    :param punctuation_to_explode_by: punctuation marks to replace with spaces
    :return: cleaned text
    """
    new_text: str = text
    # Prioritise exploding first, these are punctuation marks that the user sets
    if punctuation_to_explode_by is not '':
        pattern_to_explode_by = re.escape(punctuation_to_explode_by)
        new_text = re.sub(rf"[{pattern_to_explode_by}]", " ", new_text)
    # Then strip the rest
    if punctuation_to_collapse_by is not '':
        pattern_to_collapse_by = re.escape(punctuation_to_collapse_by)
        new_text = re.sub(rf"[{pattern_to_collapse_by}]", "", new_text)
    return new_text


def main() -> None:
    """
    Run the entire clean_json process as a command line utility.
    Usage: python3 clean_json.py [--i INFILE] [--o OUTFILE] [-r] [-u]
    """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-i", "--infile",
                        type=str,
                        help="The path to the dirty json file to clean.",
                        required=True)
    parser.add_argument("-o", "--outfile",
                        type=str,
                        help="The path to the clean json file to write to",
                        required=True)
    parser.add_argument("-r", "--remove_english",
                        help="Remove english-like utterances",
                        action="store_true")
    parser.add_argument("-u", "--use_langid",
                        help="Use langid library to detect English",
                        action="store_true")
    # TODO add defaults
    parser.add_argument("-c", "--punctuation_to_collapse_by",
                        type=str,
                        help="Chars to strip")
    parser.add_argument("-e", "--punctuation_to_explode_by",
                        type=str,
                        help="Chars to strip and replace with spaces")

    arguments = parser.parse_args()
    dirty_json_data: List[Dict[str, str]] = load_json_file(arguments.infile)
    outfile = arguments.outfile if arguments.outfile else sys.stdout

    print(f"Filtering dirty json data {arguments.infile}...")

    filtered_data = clean_json_data(json_data=dirty_json_data,
                                    remove_english=arguments.remove_english,
                                    use_langid=arguments.use_langid,
                                    punctuation_to_collapse_by=arguments.punctuation_to_collapse_by,
                                    punctuation_to_explode_by=arguments.punctuation_to_explode_by)

    write_data_to_json_file(data=list(filtered_data),
                            file_name=outfile)

    print(f"Finished! Wrote {str(len(filtered_data))} transcriptions.")


if __name__ == "__main__":
    main()
