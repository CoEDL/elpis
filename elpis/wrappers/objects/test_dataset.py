import pytest
import json
from pathlib import Path

from elpis.wrappers.objects.interface import KaldiInterface

from .dataset import Dataset

def test_new_dataset(tmpdir):
    """
    Check the state of a dataset without adding any files, selecting an
    importer or processing.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')

    # Black-box property testing
    assert ds.files == []
    assert ds.importer is None
    assert ds.has_been_processed == False

    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "importer": null
    }}
    """)

    # White-box testing, contains empty child directories "original" and
    # "resampled".
    path_to_original = Path(f'{tmpdir}/state/{ds.hash}/original')
    assert path_to_original.is_dir()
    assert [n for n in path_to_original.iterdir()] == []
    path_to_resampled = Path(f'{tmpdir}/state/{ds.hash}/resampled')
    assert path_to_resampled.is_dir()
    assert [n for n in path_to_resampled.iterdir()] == []


def test_new_dataset_using_override(tmpdir):
    """
    Using override has no effect when the dataset with the same name does not
    exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x', override=True)

    # White-box testing, contains empty child directories "original" and
    # "resampled".
    path_to_original = Path(f'{tmpdir}/state/{ds.hash}/original')
    assert path_to_original.is_dir()
    assert [n for n in path_to_original.iterdir()] == []
    path_to_resampled = Path(f'{tmpdir}/state/{ds.hash}/resampled')
    assert path_to_resampled.is_dir()
    assert [n for n in path_to_resampled.iterdir()] == []
    # Interface only has record of one dataset
    assert len(kaldi.list_datasets()) == 1


def test_new_dataset_using_use_existing(tmpdir):
    """
    Using the use_existing when an existing dataset does not exist will
    produce a RuntimeError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(RuntimeError):
        kaldi.new_dataset('dataset_x', use_existing=True)


def test_existing_dataset_using_override(tmpdir):
    """
    Use override to delete a dataset with the same name and create a totally
    new dataset with the same name.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1_hash = ds1.hash
    ds2 = kaldi.new_dataset('dataset_x', override=True)
    # note ds1 can no longer be used
    assert len(kaldi.list_datasets()) == 1
    assert ds1_hash != ds2.hash


def test_two_new_datasets_with_same_name(tmpdir):
    """
    Trying to create two datasets with the same name without override or
    use_existing set to True will produce a ValueError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    kaldi.new_dataset('dataset_x')
    with pytest.raises(ValueError):
        kaldi.new_dataset('dataset_x')


def test_existing_dataset_using_use_existing(tmpdir):
    """
    Use the use_existing parameter to load configurations from existing dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1_hash = ds1.hash
    ds2 = kaldi.new_dataset('dataset_x', use_existing=True)
    assert len(kaldi.list_datasets()) == 1
    assert ds1_hash != ds2.hash
    assert ds1.path == ds2.path


def test_override_and_use_existing(tmpdir):
    """
    Cannot have both the override and use_existing parameters set to True.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(ValueError):
        kaldi.new_dataset('dataset_x', override=True, use_existing=True)
    return

def test_select_nonexistant_importer(tmpdir):
    """
    The importer name must exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    with pytest.raises(ValueError):
        ds.import_with('this_importer_name_does_not_exist')


def test_select_importer(tmpdir):
    """
    Select an existing importer.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.import_with('Elan')
    assert ds.importer is not None
    assert ds.has_been_processed == True
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": true,
        "files": [],
        "importer": {{
            "name": "Elan",
            "import_context": {{
                "tier": "Phrase",
                "graphic": "elan.png"
            }},
            "export_context": {{
                "tier": "Phrase",
                "graphic": "elan.png"
            }}
        }}
    }}
    """)


def test_add_file(tmpdir):
    """
    Add files and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_file('/recordings/transcribed/w_1_1.wav')
    ds.add_file('/recordings/transcribed/w_1_1.eaf')
    ds.add_file('/recordings/transcribed/w_1_2.wav')
    ds.add_file('/recordings/transcribed/w_1_2.eaf')
    assert ds.importer is not None
    assert ds.has_been_processed == True
    assert ds.files == ["w_1_1.wav", "w_1_1.eaf", "w_1_2.wav", "w_1_2.eaf"]
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": ["w_1_1.wav", "w_1_1.eaf", "w_1_2.wav", "w_1_2.eaf"],
        "importer": null
    }}
    """)


def test_add_directory(tmpdir):
    """
    Add all files in a directory and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    assert ds.importer is not None
    assert ds.has_been_processed == True
    assert ds.files == [
        "w_1_1.wav",
        "w_1_1.eaf",
        "w_1_2.wav",
        "w_1_2.eaf",
        "w_1_3.wav",
        "w_1_3.eaf",
        "w_1_4.wav",
        "w_1_4.eaf"
    ]
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [
            "w_1_1.wav",
            "w_1_1.eaf",
            "w_1_2.wav",
            "w_1_2.eaf",
            "w_1_3.wav",
            "w_1_3.eaf",
            "w_1_4.wav",
            "w_1_4.eaf"
        ],
        "importer": null
    }}
    """)


def test_load(tmpdir):
    """
    Load an already existing dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds2 = Dataset.load(ds1.path)
    
    assert ds2.importer is None
    assert ds2.has_been_processed == False

def test_load_with_add_directory(tmpdir):
    """
    Add all files in a directory and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1.add_directory('/recordings/transcribed')
    ds2 = Dataset.load(ds1.path)

    assert ds2.importer is not None
    assert ds2.has_been_processed == True
    assert ds2.files == [
        "w_1_1.wav",
        "w_1_1.eaf",
        "w_1_2.wav",
        "w_1_2.eaf",
        "w_1_3.wav",
        "w_1_3.eaf",
        "w_1_4.wav",
        "w_1_4.eaf"
    ]
    assert ds2.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds1.hash}",
        "date": "{ds1.date}",
        "has_been_processed": false,
        "files": [
            "w_1_1.wav",
            "w_1_1.eaf",
            "w_1_2.wav",
            "w_1_2.eaf",
            "w_1_3.wav",
            "w_1_3.eaf",
            "w_1_4.wav",
            "w_1_4.eaf"
        ],
        "importer": null
    }}
    """)

