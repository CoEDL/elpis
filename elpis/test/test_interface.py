import pytest
from pathlib import Path

from elpis.wrappers.objects.interface import KaldiInterface


def test_construction(tmpdir):
    KaldiInterface(f"{tmpdir}/state")

    # White-box testing
    path_to_datasets = Path(f"{tmpdir}/state/datasets")
    path_to_pron_dicts = Path(f"{tmpdir}/state/pron_dicts")
    path_to_models = Path(f"{tmpdir}/state/models")
    path_to_transcriptions = Path(f"{tmpdir}/state/transcriptions")

    # Creates empty child directories:
    #   datasets/
    #   pron_dicts/
    #   models/
    #   transcriptions/
    assert path_to_datasets.is_dir()
    assert path_to_datasets.exists()
    assert [n for n in path_to_datasets.iterdir()] == []
    assert path_to_pron_dicts.is_dir()
    assert path_to_pron_dicts.exists()
    assert [n for n in path_to_pron_dicts.iterdir()] == []
    assert path_to_models.is_dir()
    assert path_to_models.exists()
    assert [n for n in path_to_models.iterdir()] == []
    assert path_to_transcriptions.is_dir()
    assert path_to_transcriptions.exists()
    assert [n for n in path_to_transcriptions.iterdir()] == []


# TODO: much more testing here
