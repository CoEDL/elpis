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
    assert ds.processed_labels == []
    assert ds.importer is None
    assert ds.has_been_processed == False

    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "processed_labels": [],
        "importer": null
    }}
    """)

    # White-box testing, contains empty child directories "original" and
    # "resampled".
    path_to_original = Path(f'{tmpdir}/state/datasets/{ds.hash}/original')
    assert path_to_original.is_dir()
    assert [n for n in path_to_original.iterdir()] == []
    path_to_resampled = Path(f'{tmpdir}/state/datasets/{ds.hash}/resampled')
    assert path_to_resampled.is_dir()
    assert [n for n in path_to_resampled.iterdir()] == []
    return

def test_protected_properties(tmpdir):
    """
    An error is raised when there is an attempt to write to a protected
    property making these properties read-only.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')

    with pytest.raises(AttributeError):
        ds.has_been_processed = True
    with pytest.raises(AttributeError):
        ds.annotations = "{}"
    with pytest.raises(AttributeError):
        ds.processed_labels = []
    with pytest.raises(AttributeError):
        ds.importer = "Not a importer"
    with pytest.raises(AttributeError):
        ds.files = []
    return


def test_new_dataset_using_override(tmpdir):
    """
    Using override has no effect when the dataset with the same name does not
    exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x', override=True)

    # White-box testing, contains empty child directories "original" and
    # "resampled".
    path_to_original = Path(f'{tmpdir}/state/datasets/{ds.hash}/original')
    assert path_to_original.is_dir()
    assert [n for n in path_to_original.iterdir()] == []
    path_to_resampled = Path(f'{tmpdir}/state/datasets/{ds.hash}/resampled')
    assert path_to_resampled.is_dir()
    assert [n for n in path_to_resampled.iterdir()] == []
    # Interface only has record of one dataset
    assert len(kaldi.list_datasets()) == 1
    return


def test_new_dataset_using_use_existing(tmpdir):
    """
    Using the use_existing when an existing dataset does not exist is okay.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x', use_existing=True)

    # Black-box property testing
    assert ds.files == []
    assert ds.processed_labels == []
    assert ds.importer is None
    assert ds.has_been_processed == False

    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "processed_labels": [],
        "importer": null
    }}
    """)
    return


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
    return


def test_two_new_datasets_with_same_name(tmpdir):
    """
    Trying to create two datasets with the same name without override or
    use_existing set to True will produce a ValueError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    kaldi.new_dataset('dataset_x')
    with pytest.raises(ValueError):
        kaldi.new_dataset('dataset_x')
    return


def test_existing_dataset_using_use_existing(tmpdir):
    """
    Use the use_existing parameter to load configurations from existing dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1_hash = ds1.hash
    ds2 = kaldi.new_dataset('dataset_x', use_existing=True)
    assert len(kaldi.list_datasets()) == 1
    assert ds1_hash == ds2.hash
    assert ds1.path == ds2.path
    return


def test_override_and_use_existing(tmpdir):
    """
    Cannot have both the override and use_existing parameters set to True.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(ValueError):
        kaldi.new_dataset('dataset_x', override=True, use_existing=True)
    return


def test_add_file(tmpdir):
    """
    Add files and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_file('/recordings/transcribed/1_1_1.wav')
    ds.add_file('/recordings/transcribed/1_1_1.eaf')
    ds.add_file('/recordings/transcribed/1_1_2.wav')
    ds.add_file('/recordings/transcribed/1_1_2.eaf')
    assert ds.files == ["1_1_1.wav", "1_1_1.eaf", "1_1_2.wav", "1_1_2.eaf"]
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": ["1_1_1.wav", "1_1_1.eaf", "1_1_2.wav", "1_1_2.eaf"],
        "processed_labels": [],
        "importer": null
    }}
    """)
    return


def test_add_directory(tmpdir):
    """
    Add all files in a directory and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    assert set(ds.files) == {
        "1_1_1.wav",
        "1_1_1.eaf",
        "1_1_2.wav",
        "1_1_2.eaf",
        "1_1_3.wav",
        "1_1_3.eaf",
        "1_1_4.wav",
        "1_1_4.eaf"
    }
    assert set(ds.state['files']) == set(json.loads(f"""
    [
        "1_1_1.wav",
        "1_1_1.eaf",
        "1_1_2.wav",
        "1_1_2.eaf",
        "1_1_3.wav",
        "1_1_3.eaf",
        "1_1_4.wav",
        "1_1_4.eaf"
    ]
    """))
    return


def test_remove_file(tmpdir):
    """
    Test that a file can be removed.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.remove_file("1_1_1.wav")
    assert set(ds.files) == {
        "1_1_1.eaf",
        "1_1_2.wav",
        "1_1_2.eaf",
        "1_1_3.wav",
        "1_1_3.eaf",
        "1_1_4.wav",
        "1_1_4.eaf"
    }
    return


def test_remove_file_that_does_not_exist(tmpdir):
    """
    Raise an error when there is an attempt to remove a file that has not been
    added.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    with pytest.raises(ValueError):
        ds.remove_file("1_1_1.wav")
    return


def test_process_then_delete_file(tmpdir):
    """
    Test when a file is removed, that the has_been_processed flag is
    switched to false as the dataset has changed.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    ds.process()
    ds.remove_file("1_1_1.wav")
    assert ds.has_been_processed == False
    return

def test_label_reset(tmpdir):
    """
    Test when a file is removed, and the has_been_processed flag is
    switched to false, that the labels are also removed.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    ds.process()
    ds.remove_file("1_1_1.wav")
    assert ds.processed_labels == []
    return


def test_load(tmpdir):
    """
    Load an already existing dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds2 = Dataset.load(ds1.path)
    
    assert ds2.importer is None
    assert ds2.has_been_processed == False
    return


def test_load_with_add_directory(tmpdir):
    """
    Add all files in a directory and see the state change.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1.add_directory('/recordings/transcribed')
    ds2 = Dataset.load(ds1.path)

    assert ds2.importer == None
    assert ds2.has_been_processed == False
    assert set(ds2.files) == {
        "1_1_1.wav",
        "1_1_1.eaf",
        "1_1_2.wav",
        "1_1_2.eaf",
        "1_1_3.wav",
        "1_1_3.eaf",
        "1_1_4.wav",
        "1_1_4.eaf"
    }
    return


def test_load_processed(tmpdir):
    """
    Load a processed dataset.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds1 = kaldi.new_dataset('dataset_x')
    ds1.add_directory('/recordings/transcribed')
    ds1.select_importer('Elan')
    ds1.process()
    ds2 = Dataset.load(ds1.path)

    assert ds2.importer is not None
    assert ds2.has_been_processed == True
    assert set(ds2.processed_labels) == set(["1_1_1", "1_1_2", "1_1_3", "1_1_4"])
    return


def test_select_nonexistant_importer(tmpdir):
    """
    The importer name must exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    with pytest.raises(ValueError):
        ds.select_importer('this_importer_name_does_not_exist')
    return


def test_select_importer(tmpdir):
    """
    Select an existing importer.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.select_importer('Elan')
    assert ds.importer is not None
    assert ds.has_been_processed == False
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "processed_labels": [],
        "importer": {{
            "name": "Elan",
            "context": {{
                "tier": "Phrase",
                "graphic": "elan.png"
            }}
        }}
    }}
    """)
    return

def test_change_importer_setting(tmpdir):
    """
    Change a property of the importer.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.select_importer('Elan')
    ds.importer.context["tier"] = "Shift"
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "processed_labels": [],
        "importer": {{
            "name": "Elan",
            "context": {{
                "tier": "Shift",
                "graphic": "elan.png"
            }}
        }}
    }}
    """)
    return

def test_select_importer_when_already_selected(tmpdir):
    """
    Re-specify the importer will clear settings back to the default.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.select_importer('Elan')
    ds.importer.context["tier"] = "Shift"
    ds.select_importer('Elan')
    assert ds.state == json.loads(f"""
    {{
        "name": "dataset_x",
        "hash": "{ds.hash}",
        "date": "{ds.date}",
        "has_been_processed": false,
        "files": [],
        "processed_labels": [],
        "importer": {{
            "name": "Elan",
            "context": {{
                "tier": "Phrase",
                "graphic": "elan.png"
            }}
        }}
    }}
    """)
    return

def test_change_setting_before_selecting_importer(tmpdir):
    """
    If an attempt to change a setting of the importer is made, then an error
    will be raised.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    with pytest.raises(AttributeError): # importer is None
        ds.importer.context["tier"] = "Shift"
    return

def test_process(tmpdir):
    """
    Process the dataset (import and generate wordlist).
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    ds.process()

    # Blackbox test
    assert ds.has_been_processed == True
    assert ds.state["has_been_processed"] == True

    # Whitebox tests
    annotations_path = Path(f'{ds.path}/annotations.json')
    assert annotations_path.is_file()
    word_list_path = Path(f'{ds.path}/word_list.txt')
    assert word_list_path.is_file()
    return

def test_annotations_before_processing(tmpdir):
    """
    If there is an attempt to collect the annotations before processing the
    data (annotationts cannot exist), an error will be raised,
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    with pytest.raises(RuntimeError):
        _ = ds.annotations
    return

def test_annotations_after_processing(tmpdir):
    """
    Ensure annotations are retrievable.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_directory('/recordings/transcribed')
    ds.select_importer('Elan')
    ds.process()
    annotations = ds.annotations
    # ensure no errors are raised. annotations is JSONable
    assert len(annotations) != 0
    return


def test_process_without_importer(tmpdir):
    """
    Running the process() function without specifying an importer from the
    available data transformers will raise an error.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    with pytest.raises(RuntimeError):
        ds.process()
    return


def test_add_directory_after_process(tmpdir):
    """
    When files are added after processing, the dataset attains the state of
    being unprocessed.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_file('/recordings/transcribed/1_1_1.wav')
    ds.add_file('/recordings/transcribed/1_1_1.eaf')
    ds.select_importer('Elan')
    ds.process()
    assert ds.has_been_processed == True
    ds.add_file('/recordings/transcribed/1_1_2.wav')
    ds.add_file('/recordings/transcribed/1_1_2.eaf')
    assert ds.has_been_processed == False
    assert set(ds.processed_labels) == set()
    return


def test_process_empty_dataset(tmpdir):
    """
    Attempting to process a dataset with no files will not produce an error.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.select_importer('Elan')
    ds.process()
    return

def test_mismatched_audio_and_transcription_files(tmpdir):
    """
    Only process associated pairs.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    ds.add_file('/recordings/transcribed/1_1_1.wav')
    ds.add_file('/recordings/transcribed/1_1_2.wav')
    ds.add_file('/recordings/transcribed/1_1_2.eaf')
    ds.add_file('/recordings/transcribed/1_1_3.eaf')
    ds.select_importer('Elan')
    ds.process()
    assert ds.has_been_processed == True
    assert set(ds.processed_labels) == {"1_1_2"}
    return

# TODO: White-box test the state of the annotations.json file and how it is accessed.