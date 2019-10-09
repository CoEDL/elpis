import pytest
import json
from pathlib import Path

from elpis.wrappers.objects.interface import KaldiInterface

# from .test_pipeline import pipeline_upto_step_3

import test_pipeline


def test_new_transcription(tmpdir):
    """
    Check the state of a new transcription.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t = kaldi.new_transcription('transcription_w')
    assert t.has_been_transcribed == False
    assert t.exporter == None
    assert t.state == json.loads(f"""
    {{
        "name": "transcription_w",
        "hash": "{t.hash}",
        "model": null,
        "has_been_transcribed": false,
        "exporter": null
    }}
    """)
    return


def test_error_when_writing_to_protected_property(tmpdir):
    """
    An error is raised when there is an attempt to write to a protected
    property.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t = kaldi.new_transcription('transcription_w')

    with pytest.raises(NotImplementedError):
        t.has_been_transcribed = True
    with pytest.raises(NotImplementedError):
        t.exporter = "some obj"
    with pytest.raises(NotImplementedError):
        t.state = "Not a valid"
    with pytest.raises(NotImplementedError):
        t.model = "must link a model not assign it"


def test_new_transcription_using_override(tmpdir):
    """
    Using override has no effect when the pron dict with the same name does not
    exist.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t = kaldi.new_transcription('transcription_w', override=True)
    assert t.has_been_transcribed == False
    assert t.exporter == None
    assert t.state == json.loads(f"""
    {{
        "name": "transcription_w",
        "hash": "{t.hash}",
        "model": null,
        "has_been_transcribed": false,
        "exporter": null
    }}
    """)
    return


def test_new_transcription_using_use_existing(tmpdir):
    """
    Using the use_existing when an existing transcription does not exist will
    produce a RuntimeError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(RuntimeError):
        kaldi.new_transcription('transcription_w', use_existing=True)
    return


def test_existing_transcription_using_override(tmpdir):
    """
    Use override to delete a transcription with the same name and create a totally
    new transcription with the same name.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t1 = kaldi.new_transcription('transcription_w')
    t1_hash = t1.hash
    t2 = kaldi.new_transcription('transcription_w', override=True)
    # note t1 can no longer be used
    assert len(kaldi.list_transcriptions()) == 1
    assert t1_hash != t2.hash
    return


def test_two_new_transcription_with_same_name(tmpdir):
    """
    Trying to create two transcriptions with the same name without override or
    use_existing set to True will produce a ValueError.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    kaldi.new_transcription('transcription_w')
    with pytest.raises(ValueError):
        kaldi.new_transcription('transcription_w')
    return


def test_existing_transcription_using_use_existing(tmpdir):
    """
    Use the use_existing parameter to load configurations from existing pron dict.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t1 = kaldi.new_transcription('transcription_w')
    t1_hash = t1.hash
    t2 = kaldi.new_transcription('transcription_w', use_existing=True)
    assert len(kaldi.list_transcriptions()) == 1
    assert t1_hash != t2.hash
    assert t1.path == t2.path
    return


def test_override_and_use_existing(tmpdir):
    """
    Cannot have both the override and use_existing parameters set to True.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    with pytest.raises(ValueError):
        kaldi.new_transcription('transcription_w', override=True, use_existing=True)
    return


def test_linking(pipeline_upto_step_3):
    """
    Check state after linking.
    """
    kaldi, ds, pd, m = pipeline_upto_step_3
    t = kaldi.new_transcription('transcription_w')
    t.link(m)
    assert t.model == 'model_z'
    return


def test_transcribe_before_linking(tmpdir):
    """
    Generating an inference file before linking is not permitted and produces
    an error.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    t = kaldi.new_transcription('transcription_w')
    with pytest.raises(RuntimeError):
        t.transcribe_to_text('/recordings/untranscribed/audio.wav')
    with pytest.raises(RuntimeError):
        t.transcribe_align('/recordings/untranscribed/audio.wav')
    return


def test_transcribe_to_text(pipeline_upto_step_3):
    """
    Test if some audio can be transcribed into plane text.
    """
    kaldi, ds, pd, m = pipeline_upto_step_3
    t = kaldi.new_transcription('transcription_w')
    t.link(m)
    text = t.transcribe_to_text('/recordings/untranscribed/audio.wav')
    assert text is str
    assert len(text) > 0
    # only transcribe_align chages this flag to True
    assert t.has_been_transcribed == False


def test_transcribe_align(pipeline_upto_step_3):
    """
    Test if some audio can be transcribed into some aligned utterances.
    """
    kaldi, ds, pd, m = pipeline_upto_step_3
    t = kaldi.new_transcription('transcription_w')
    t.link(m)
    t.transcribe_align('/recordings/untranscribed/audio.wav')
    # Black-box testing
    assert t.has_been_transcribed == True

    # White-box testing: theck the inner content for CTM



def test_default_exporter(tmpdir):
    """
    After linking test if the default exporter is derived.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    t = kaldi.new_transcription('transcription_w')
    pass


def test_default_exporter_importer_only(tmpdir):
    """
    Sometimes a dataset will have a data transformer that is import only
    (exporting is disabled). Ensure the exporter in the transcription is
    nullified.
    """
    kaldi = KaldiInterface(f'{tmpdir}/state')
    ds = kaldi.new_dataset('dataset_x')
    t = kaldi.new_transcription('transcription_w')
    pass


def test_set_exporter(tmpdir):
    """
    Set a new exporter.
    """
    pass

def test_set_exporter_same_type(tmpdir):
    """
    Set a new exporter of the same type as the default. This should clear the
    context.
    """
    pass


def test_set_exporter_with_importer_only(tmpdir):
    """
    Setting an exporter when it is an importer only will raise an error.
    """
    pass

def test_use_exporter(tmpdir):
    """
    Use an exporter to produce a transcription file
    """