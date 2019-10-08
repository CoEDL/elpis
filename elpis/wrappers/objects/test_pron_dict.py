import pytest
import json
from pathlib import Path

from elpis.wrappers.objects.interface import KaldiInterface

from .pron_dict import PronDict


def test_new_pron_dict(tmpdir):
    """
    Check the state of a new pron dict.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    # ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    assert pd.get_l2s_content() == False
    assert pd.get_lexicon_content() == 'No lexicon yet'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": null,
        "l2s": false,
        "lexicon": false
    }}
    """)
    return

def test_new_pron_dict_using_override(tmpdir):
    """
    Using override has no effect when the pron dict with the same name does not
    exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd = kaldi.new_pron_dict('pronunciation dictionary', override=True)
    assert pd.get_l2s_content() == False
    assert pd.get_lexicon_content() == 'No lexicon yet'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": null,
        "l2s": false,
        "lexicon": false
    }}
    """)
    return


def test_new_dataset_using_use_existing(tmpdir):
    """
    Using the use_existing when an existing dataset does not exist will
    produce a RuntimeError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(RuntimeError):
        kaldi.new_dataset('dataset_x', use_existing=True)
    return


def test_existing_pron_dict_using_override(tmpdir):
    """
    Use override to delete a pron dict with the same name and create a totally
    new dataset with the same name.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd1 = kaldi.new_pron_dict('pronunciation dictionary')
    pd1_hash = pd1.hash
    pd2 = kaldi.new_pron_dict('pronunciation dictionary', override=True)
    # note pd1 can no longer be used
    assert len(kaldi.list_pron_dicts()) == 1
    assert pd1_hash != pd2.hash
    return


def test_two_new_pron_dict_with_same_name(tmpdir):
    """
    Trying to create two pron dict with the same name without override or
    use_existing set to True will produce a ValueError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    kaldi.new_pron_dict('p')
    with pytest.raises(ValueError):
        kaldi.new_pron_dict('p')
    return


def test_existing_pron_dict_using_use_existing(tmpdir):
    """
    Use the use_existing parameter to load configurations from existing pron dict.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd1 = kaldi.new_pron_dict('x')
    pd1_hash = ds1.hash
    pd2 = kaldi.new_pron_dict('x', use_existing=True)
    assert len(kaldi.list_pron_dicts()) == 1
    assert pd1_hash != pd2.hash
    assert pd1.path == pd2.path
    return


def test_override_and_use_existing(tmpdir):
    """
    Cannot have both the override and use_existing parameters set to True.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(ValueError):
        kaldi.new_pron_dict('x', override=True, use_existing=True)
    return

def test_pron_dict_with_dataset(tmpdir):
    """
    Link dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.link(ds)

    assert pd.get_lexicon_content() == 'No lexicon yet'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": "dataset_x",
        "l2s": false,
        "lexicon": false
    }}
    """)
    return


def test_set_l2s_missing_path(tmpdir):
    """
    If the path does not exist then get a missing file error.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    with pytest.raises(FileNotFoundError):
        pd.set_l2s_path('/missing/letter_to_sound.txt')
    return


def test_set_l2s_content(tmpdir):
    """
    Set letters to sound by content.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    with open('/recordings/letter_to_sound.txt', 'r') as fin():
        content = fin.read()
        pd.set_l2s_content(content)
    
    assert pd.get_lexicon_content() != 'No lexicon yet'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": null,
        "l2s": true,
        "lexicon": false
    }}
    """)
    return


def test_set_l2s_path(tmpdir):
    """
    Set letters to sound by file path.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    
    assert pd.get_lexicon_content() != 'No lexicon yet'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": null,
        "l2s": true,
        "lexicon": false
    }}
    """)
    return

def test_lexicon(tmpdir):
    """
    Generate lexicon.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()

    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": "dataset_x",
        "l2s": true,
        "lexicon": true
    }}
    """)
    return


def test_lexicon_without_l2s(tmpdir):
    """
    Attempt to generate lexicon without letters to sound will result in error.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.link(ds)

    with pytest.raises(RuntimeError):
        pd.generate_lexicon()
    return

def test_save_lexicon(tmpdir):
    """
    save a lexicon separate from the letters to sounds.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.save_lexicon('This is the new lexicon')
    assert pd.get_lexicon_content() == 'This is the new lexicon'
    assert pd.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd.hash}",
        "dataset": null,
        "l2s": false,
        "lexicon": true
    }}
    """)
    return


def test_loads_minimal(tmpdir):
    """
    Use load class method to load a pron dict from existing configuration.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    pd1 = kaldi.new_pron_dict('pronunciation dictionary')
    pd2 = PronDict.loads(pd1.path)

    assert pd2.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd1.hash}",
        "dataset": null,
        "l2s": false,
        "lexicon": false
    }}
    """)
    return


def test_loads_minimal(tmpdir):
    """
    Use load class method to load a pron dict from existing configuration. All variables set.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    pd = kaldi.new_pron_dict('pronunciation dictionary')
    pd.link(ds)
    pd.set_l2s_path('/recordings/letter_to_sound.txt')
    pd.generate_lexicon()
    pd2.loads(pd1.path)

    assert pd2.state == json.loads(f"""
    {{
        "name": "pronunciation dictionary",
        "hash": "{pd1.hash}",
        "dataset": "dataset_x",
        "l2s": true,
        "lexicon": true
    }}
    """)
    return
