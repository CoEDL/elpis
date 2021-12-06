#!/usr/bin/python3

"""
Copyright: University of Queensland, 2019
Contributors:
              Josh Arnold - (The University of Queensland, 2017)
              Ben Foley - (The University of Queensland, 2018)
              Nicholas Lambourne - (The University of Queensland, 2019)
              Nicholas Buckeridge - (The University of Queensland, 2019)
"""

from loguru import logger
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
from typing import Callable, Dict, List, Set, Tuple
from pathlib import Path

from elpis.engines.common.input.clean_json import clean_json_utterance

from elpis.transformer import DataTransformerAbstractFactory

elan = DataTransformerAbstractFactory('Elan')


elan.set_audio_extention('wav')

DEFAULT_TIER = 'Phrase'
GRAPHIC_RESOURCE_NAME = 'elan.png'

elan.set_default_context({
    # 'tier': DEFAULT_TIER,
    'graphic': GRAPHIC_RESOURCE_NAME
})


# TODO: ensure the order the settings are defined in is the order they are shown in. Also document this behaviour

elan.general_setting_title(title='tiers')
elan.general_setting(key='selection_mechanism',
                     ui_format='select',
                     display_name='selectionMechanism',
                     options=['tier_name', 'tier_type', 'tier_order'],
                     default='tier_name')
elan.general_setting(key='tier_name',
                     ui_format='select',
                     display_name='name',
                     options=[],
                     shown=False)
elan.general_setting(key='tier_type',
                     ui_format='select',
                     display_name='type',
                     options=[],
                     shown=False)
elan.general_setting(key='tier_order',
                     ui_format='select',
                     display_name='order',
                     options=[],
                     shown=False)

elan.general_setting_title(title='punctuation')
elan.general_setting(key='punctuation_to_explode_by',
                     ui_format='text',
                     display_name='explosion',
                     default=string.punctuation + ',…‘’“”°')
elan.general_setting(key='punctuation_to_collapse_by',
                     ui_format='text',
                     display_name='collapsing',
                     default='')

# These settings are string that end up being converted to sets
elan.general_setting_title(title='cleaning')
elan.general_setting(key='special_cases',
                     ui_format='textarea',
                     display_name='words',
                     default="<silence>")
elan.general_setting(key='translation_tags',
                     ui_format='textarea',
                     display_name='tags',
                     default="@eng@")

# TODO: limitation, settings must be defined before used in functions so that they are registered and visible.


# @elan.update_ui
# def update_ui(file_paths, ui):
#     tier_types, tier_names, tier_max_count = get_elan_tier_attributes(file_paths)

#     return ui

@elan.validate_files('eaf')
def elan_validator(file_paths: List[Path]):
    logger.info(f"validating: {file_paths}")
    return None

@elan.update_ui
def update_ui(file_paths: List[Path], ui):
    """
    Iterate a dir of elan files and compiles info about all the files' tiers:
    unique tier types, unique tier names, and the num of tiers
    """
    # Use sets internally for easy uniqueness, conver to lists when done
    _tier_types: Set[str] = set(ui['data']['tier_type']['options'])
    _tier_names: Set[str] = set(ui['data']['tier_name']['options'])
    tier_max_count = 0

    logger.info('**** ui data')
    logger.info(ui['data'])

    logger.info('**** _tier_types')
    logger.info(_tier_types)

    eaf_paths = [p for p in file_paths if f'{p}'.endswith('.eaf')]
    for eaf_path in eaf_paths:
        input_eaf = Eaf(eaf_path)
        for tier_type in list(input_eaf.get_linguistic_type_names()):
            _tier_types.add(tier_type)
            tier_ids: List[str] = input_eaf.get_tier_ids_for_linguistic_type(
                tier_type)
            for tier_id in tier_ids:
                _tier_names.add(tier_id)
        # count the number of tiers, use the max from all files
        tier_count = len(list(input_eaf.get_tier_names()))
        if tier_count > tier_max_count:
            tier_max_count = tier_count

    ui['data']['tier_type']['options'] = list(_tier_types)
    ui['data']['tier_name']['options'] = list(_tier_names)
    ui['data']['tier_order']['options'] = [i for i in range(tier_max_count)]
    return ui

@elan.import_files('eaf')
def import_eaf_file(eaf_paths: List[str],
                    context: Dict[str, str],
                    reset_annotations: Callable,
                    add_annotation: Callable,
                    tmp_dir):
    """
    Import handler for processing .eaf files.

    :param eaf_paths: List of string paths to Elan files.
    :param context: The settings that will be used to process data from the Elan files.
    :param reset_annotations: Callback to wipe all annotations that have been previously read.
        Settings such as the tier type/name/order will determine which annotations are read
        into the dataset _annotation_store. When settings are changed—
        (Wait, what? Users change their minds?? OMG yes.)
        —reset_annotations will reset dataset _annotation_store to {}, ready for annotations derived from the new
        settings to be added. Without this, changing settings will result in annotations derived from application
        of new settings being appended to previous annotations.
    :param add_annotation: Callback to append an annotation from selected tier
    :param tmp_dir: Honestly, no idea...
    """

    tier_order = context['tier_order']
    tier_name = context['tier_name']
    tier_type = context['tier_type']
    punctuation_to_collapse_by = context['punctuation_to_collapse_by']
    punctuation_to_explode_by = context['punctuation_to_explode_by']
    special_cases = set(context['special_cases'].splitlines())
    translation_tags = set(context['translation_tags'].splitlines())

    reset_annotations()

    for input_elan_file in eaf_paths:
        # Get paths to files
        input_directory, full_file_name = os.path.split(input_elan_file)
        file_name, extension = os.path.splitext(full_file_name)

        input_eaf = Eaf(input_elan_file)
        tier_types: List[str] = list(input_eaf.get_linguistic_type_names())
        tier_names: List[str] = list(input_eaf.get_tier_names())

        # Get annotations and parameters (things like speaker id) on the target tier
        annotations: List[Tuple[str, str, str]] = []
        annotation_data: List[dict] = []

        # Try using tier_order. Watch out for mixed type, empty str if not selected, int if selected
        if isinstance(tier_order, int):
            try:
                tier_name = tier_names[tier_order]
                logger.info(f"using tier order {tier_order} to get tier name {tier_name}")
            except IndexError:
                logger.warning("couldn't find a tier")
                pass
        else:
            # else use tier type to get a tier name
            if tier_type in tier_types:
                logger.info(f"found tier type {tier_type}")
                tier_names = input_eaf.get_tier_ids_for_linguistic_type(tier_type)
                tier_name = tier_names[0]
                if tier_name:
                    logger.info(f"found tier name {tier_name}")
            else:
                logger.warning("tier type not found in this file")

        if tier_name in tier_names:
            logger.info(f"using tier name {tier_name}")
            annotations = input_eaf.get_annotation_data_for_tier(tier_name)
        else:
            pass  # TODO: Alert user of a skip due to missing tier_name in file

        if annotations:
            annotations = sorted(annotations)
            parameters: Dict[str,str] = input_eaf.get_parameters_for_tier(tier_name)
            speaker_id: str = parameters.get("PARTICIPANT", "")

        for annotation in annotations:
            start = annotation[0]
            end = annotation[1]
            annotation = annotation[2]

            utterance = {
                "audio_file_name": f"{file_name}.wav",
                "transcript": annotation,
                "start_ms": start,
                "stop_ms": end,
                "speaker_id": speaker_id
            }

            utterance_cleaned = clean_json_utterance(utterance=utterance,
                                                     punctuation_to_collapse_by=punctuation_to_collapse_by,
                                                     punctuation_to_explode_by=punctuation_to_explode_by,
                                                     special_cases=special_cases,
                                                     translation_tags=translation_tags,
                                                     remove_english=False,
                                                     use_langid=False)
            add_annotation(file_name, utterance_cleaned)


def get_elan_tier_attributes(input_eafs_files):
    """
    Iterate a dir of elan files and compiles info about all the files' tiers:
    unique tier types, unique tier names, and the num of tiers
    """
    # Use sets internally for easy uniqueness, conver to lists when done
    _tier_types: Set[str] = set()
    _tier_names: Set[str] = set()
    _tier_max_count: int = 0
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
        if tier_count > _tier_max_count:
            _tier_max_count = tier_count
    tier_types = list(_tier_types)
    tier_names = list(_tier_names)
    tier_max_count = _tier_max_count
    return (tier_types, tier_names, tier_max_count)