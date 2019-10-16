import pytest
import json
from pathlib import Path

from . import DataTransformer, DataTransformerAbstractFactory

TEST_FACTORY_TDTAF = '__TEST__TEMP_FACTORY_TDTAF'

@pytest.fixture
def remove_dtaf():
    """
    A pytest fixture that stores the collection of DataTransformerAbstractFactory
    names before the test is run, then deletes any DataTransformerAbstractFactory
    that were created for the test when the test ends.
    """
    s_before = set(DataTransformerAbstractFactory._transformer_factories.keys())
    yield None
    s_after = set(DataTransformerAbstractFactory._transformer_factories.keys())
    for name in (s_after - s_before):
        DataTransformerAbstractFactory._transformer_factories.pop(name)
    return


@pytest.fixture
def tdtaf(remove_dtaf):
    """
    A pytest fixture that yields a temporary Test DataTransformerAbstractFactory
    (tdtaf) that lives as long as the test runs.
    """
    return DataTransformerAbstractFactory(TEST_FACTORY_TDTAF)


###############################################################################
####                               Test Factory                            ####
###############################################################################

def test_factory_new(remove_dtaf):
    """
    Check if a new factory can be created.
    """
    TEST_FACTORY_NAME_CREATE = '__TEST_FACTORY_CREATE_TEST'
    DataTransformerAbstractFactory(TEST_FACTORY_NAME_CREATE)

    # White-box testing
    assert TEST_FACTORY_NAME_CREATE in DataTransformerAbstractFactory._transformer_factories
    t = type(DataTransformerAbstractFactory._transformer_factories[TEST_FACTORY_NAME_CREATE])
    assert t == DataTransformerAbstractFactory
    return


def test_factory_new_twice(remove_dtaf):
    """
    Check if a two new factories can be created.
    """
    DataTransformerAbstractFactory('__TEST_FACTORY_1')
    DataTransformerAbstractFactory('__TEST_FACTORY_2')

    # White-box testing
    names = DataTransformerAbstractFactory._transformer_factories.keys()
    assert '__TEST_FACTORY_1' in names
    assert '__TEST_FACTORY_2' in names
    return


def test_factory_same_name(remove_dtaf):
    """
    Raise an error when a new factory is created with an existing name.
    """
    DataTransformerAbstractFactory('__TEST_FACTORY_SAME_NAME')
    with pytest.raises(ValueError):
        DataTransformerAbstractFactory('__TEST_FACTORY_SAME_NAME')
    return


def test_factory_audio_extention(tdtaf):
    """
    Check the setting and getting of the audio extentions.
    """
    assert tdtaf.get_audio_extention() == 'wav'
    tdtaf.set_audio_extention('mp3')
    assert tdtaf.get_audio_extention() == 'mp3'
    return


def test_factory_default_context(tdtaf):
    """
    Check the default default context for importers and exporters is the empty
    {}.
    """
    assert tdtaf._import_context == {}
    assert tdtaf._export_context == {}
    return


def test_factory_set_default_context(tdtaf):
    """
    Check the setting of the default context for importers and exporters.
    """
    tdtaf.set_default_context({
        'field1': 'value1',
        'field2': 'value2'
    })
    assert tdtaf._import_context == {
        'field1': 'value1',
        'field2': 'value2'
    }
    assert tdtaf._export_context == {
        'field1': 'value1',
        'field2': 'value2'
    }
    return


def test_factory_set_default_context_copy(tdtaf):
    """
    Check the setting of the default context for importers and exporters is a
    copy.
    """
    d = {
        'field1': 'value1',
        'field2': 'value2'
    }
    tdtaf.set_default_context(d)
    assert tdtaf._import_context is not d
    assert tdtaf._export_context is not d
    assert tdtaf._import_context is not tdtaf._export_context
    return


def test_factory_set_default_context_twice(tdtaf):
    """
    Attempting to set a default context twice is ambiguous and will raise an
    error.
    """
    tdtaf.set_default_context({})
    with pytest.raises(RuntimeError):
        tdtaf.set_default_context({})
    return


def test_factory_set_default_context_non_json(tdtaf):
    """
    Non-JSONable types will raise an error.
    """
    class Obj: # Non-JSONable type
        pass
    with pytest.raises(TypeError):
        tdtaf.set_default_context({'obj': Obj()})
    return


###############################################################################
####                          Test Import Decorators                       ####
###############################################################################

def test_factory_import_files(tdtaf):
    """
    Test if the import_files fucntion can be registerd.
    """
    @tdtaf.import_files('test')
    def import_test_files(file_paths, context, add_annotation):
        pass
    # White-box testing
    assert 'import_test_files' in tdtaf._attributes
    assert 'test' in tdtaf._import_extension_callbacks
    assert tdtaf._attributes['import_test_files'] is import_test_files
    return


def test_factory_import_files_correct_arguments(tdtaf):
    """
    Test if the import_files decorator raises an error when the arguments of
    the decorated function are not correct.
    """
    with pytest.raises(RuntimeError):
        @tdtaf.import_files('test')
        def import_test_files(must, have, three, arguments, only): # pylint: disable=unused-variable
            pass
    return

def test_factory_import_files_twice(tdtaf):
    """
    Test if the import_files fucntion can be registerd twice on different file
    extentions.
    """

    # Black-box testing
    @tdtaf.import_files('test1')
    def import_test1_files(file_paths, context, add_annotation): # pylint: disable=unused-variable
        pass

    @tdtaf.import_files('test2')
    def import_test2_files(file_paths, context, add_annotation): # pylint: disable=unused-variable
        pass

    # White-box testing
    assert 'import_test1_files' in tdtaf._attributes
    assert 'import_test2_files' in tdtaf._attributes
    assert 'test1' in tdtaf._import_extension_callbacks
    assert 'test2' in tdtaf._import_extension_callbacks
    return


def test_factory_import_files_twice_same_ext(tdtaf):
    """
    Test if when the import_files fucntion can be registerd twice on the same
    file extentions, an error is raised.
    """
    @tdtaf.import_files('test')
    def import_test_files1(a, b, c): # pylint: disable=unused-variable
        pass

    with pytest.raises(RuntimeError):
        @tdtaf.import_files('test')
        def import_test_files2(a, b, c): # pylint: disable=unused-variable
            pass
    return


def test_factory_import_directory(tdtaf):
    """
    Test if the import_directory fucntion can be registerd.
    """
    @tdtaf.import_directory
    def import_test_dir(dir_path, context, add_annotation, add_audio):
        pass
    # White-box testing
    assert 'import_test_dir' in tdtaf._attributes
    assert tdtaf._import_directory_callback is import_test_dir
    return


def test_factory_import_directory_correct_arguments(tdtaf):
    """
    Test if the import_directory decorator raises an error when the arguments of
    the decorated function are not correct.
    """
    with pytest.raises(RuntimeError):
        @tdtaf.import_directory
        def import_test_dir(must, have, four, arguments, only): # pylint: disable=unused-variable
            pass
    return


def test_factory_import_directory_twice(tdtaf):
    """
    Raise an error if the import_directory decorator is used twice. On
    importing a directory, it would be ambiguous as to which funciton to use.
    """
    @tdtaf.import_directory
    def f1(a, b, c, d): # pylint: disable=unused-variable
        pass
    
    with pytest.raises(RuntimeError):
        @tdtaf.import_directory
        def f2(a, b, c, d): # pylint: disable=unused-variable
            pass
    return


def test_factory_import_files_import_directory(tdtaf):
    """
    If import_files and import_directory decorators are used together then
    raise an error. It becomes ambiguous as to which one to use.
    """
    @tdtaf.import_files('test')
    def f1(a, b, c): # pylint: disable=unused-variable
        pass
    
    with pytest.raises(RuntimeError):
        @tdtaf.import_directory
        def f2(a, b, c, d): # pylint: disable=unused-variable
            pass
    return


def test_factory_import_directory_import_files(tdtaf):
    """
    If import_files and import_directory decorators are used together then
    raise an error. It becomes ambiguous as to which one to use. Test other
    way to test_factory_import_files_import_directory.
    """
    @tdtaf.import_directory
    def f1(a, b, c, d): # pylint: disable=unused-variable
        pass
    
    with pytest.raises(RuntimeError):
        @tdtaf.import_files('test')
        def f2(a, b, c): # pylint: disable=unused-variable
            pass
    return


###############################################################################
####                          Test Export Decorators                       ####
###############################################################################

def test_factory_export(tdtaf):
    """
    Test if a function using the export decorator can be registerd.
    """
    @tdtaf.export
    def export(annotations, context, output_dir):
        pass
    # White-box testing
    assert 'export' in tdtaf._attributes
    assert tdtaf._export_callback is export
    assert tdtaf._attributes['export'] is export
    return


def test_factory_export_files_twice(tdtaf):
    """
    Raise an error if the export deforator is used more than once. Specifying
    two export functions makes choosing between them ambiguous.
    """

    @tdtaf.export
    def export1(annotations, context, output_dir): # pylint: disable=unused-variable
        pass

    with pytest.raises(RuntimeError):
        @tdtaf.export
        def export2(annotations, context, output_dir): # pylint: disable=unused-variable
            pass
    return


###############################################################################
####                           Test Import Settings                        ####
###############################################################################

def test_factory_import_setting(tdtaf):
    """
    Test if the import_setting fucntion can be registerd.
    """
    tdtaf.import_setting('field1', str)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': None
    }
    assert tdtaf._export_ui_config == {}
    assert tdtaf._export_context == {}
    return

def test_factory_import_setting_with_default(tdtaf):
    """
    Check the default value is stored correctly.
    """
    tdtaf.import_setting('field1', str, default='value1')
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': 'value1'
    }
    assert tdtaf._export_ui_config == {}
    assert tdtaf._export_context == {}
    return

def test_factory_import_setting_with_ui(tdtaf):
    """
    Check the default value is ui.
    """
    ui_config = {
        'type': 'textbox',
        'label': 'field1',
        'placeholder': 'e.g. value here'
    }
    tdtaf.import_setting('field1', str, ui=ui_config)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': {
                'type': 'textbox',
                'label': 'field1',
                'placeholder': 'e.g. value here'
            }
        }
    }
    assert tdtaf._import_context == {
        'field1': None
    }
    assert tdtaf._export_ui_config == {}
    assert tdtaf._export_context == {}
    return


def test_factory_import_setting_conflict_default_config(tdtaf):
    """
    If a key in the default config is set, an error should be raised if there
    is an attempt to create a setting with a name that is in the list of keys.
    """
    tdtaf.set_default_context({
        'field1': 'value1'
    })
    with pytest.raises(ValueError):
        tdtaf.import_setting('field1', str)
    return


def test_factory_import_setting_twice(tdtaf):
    """
    Check if two import settings can be specified.
    """
    tdtaf.import_setting('field1', str)
    tdtaf.import_setting('field2', str)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        },
        'field2': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': None,
        'field2': None
    }
    assert tdtaf._export_ui_config == {}
    assert tdtaf._export_context == {}
    return


def test_factory_import_setting_same_field_name(tdtaf):
    """
    Raise an error if import_settings is used twice with the same field name.
    """
    tdtaf.import_setting('field1', str)
    with pytest.raises(ValueError):
        tdtaf.import_setting('field1', str)
    return


def test_factory_import_capable_default(tdtaf):
    """
    Without specifying an importing function, the DataTransformer is not
    import capable.
    """
    assert tdtaf.is_import_capable() == False
    return


def test_factory_import_files_import_capable(tdtaf):
    """
    Specifying an import_files decorated function will make the DataTransformer
    import capable.
    """
    @tdtaf.import_files('test')
    def import_test_files(a, b, c): # pylint: disable=unused-variable
        pass
    assert tdtaf.is_import_capable() == True
    return


def test_factory_import_directory_import_capable(tdtaf):
    """
    Specifying an import_directory decorated function will make the DataTransformer
    import capable.
    """
    @tdtaf.import_directory
    def import_test_dir(a, b, c): # pylint: disable=unused-variable
        pass
    assert tdtaf.is_import_capable() == True
    return


###############################################################################
####                           Test Export Settings                        ####
###############################################################################

def test_factory_export_setting(tdtaf):
    """
    Test if the export_setting fucntion can be registerd.
    """
    tdtaf.export_setting('field1', str)
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': None
    }
    assert tdtaf._import_ui_config == {}
    assert tdtaf._import_context == {}
    return

def test_factory_export_setting_with_default(tdtaf):
    """
    Check the default value is stored correctly.
    """
    tdtaf.export_setting('field1', str, default='value1')
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': 'value1'
    }
    assert tdtaf._import_ui_config == {}
    assert tdtaf._import_context == {}
    return

def test_factory_export_setting_with_ui(tdtaf):
    """
    Check the default value is ui.
    """
    ui_config = {
        'type': 'textbox',
        'label': 'field1',
        'placeholder': 'e.g. value here'
    }
    tdtaf.export_setting('field1', str, ui=ui_config)
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': {
                'type': 'textbox',
                'label': 'field1',
                'placeholder': 'e.g. value here'
            }
        }
    }
    assert tdtaf._export_context == {
        'field1': None
    }
    assert tdtaf._import_ui_config == {}
    assert tdtaf._import_context == {}
    return


def test_factory_export_setting_conflict_default_config(tdtaf):
    """
    If a key in the default config is set, an error should be raised if there
    is an attempt to create a setting with a name that is in the list of keys.
    """
    tdtaf.set_default_context({
        'field1': 'value1'
    })
    with pytest.raises(ValueError):
        tdtaf.export_setting('field1', str)
    return


def test_factory_export_setting_twice(tdtaf):
    """
    Check if two export settings can be specified.
    """
    tdtaf.export_setting('field1', str)
    tdtaf.export_setting('field2', str)
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        },
        'field2': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': None,
        'field2': None
    }
    assert tdtaf._import_ui_config == {}
    assert tdtaf._import_context == {}
    return


def test_factory_export_setting_same_field_name(tdtaf):
    """
    Raise an error if export_settings is used twice with the same field name.
    """
    tdtaf.export_setting('field1', str)
    with pytest.raises(ValueError):
        tdtaf.export_setting('field1', str)
    return


def test_factory_export_capable_default(tdtaf):
    """
    Without specifying an export decorated function the DataTransformer is not
    export capable.
    """
    assert tdtaf.is_export_capable() == False
    return


def test_factory_export_export_capable(tdtaf):
    """
    Specifying an export decorated function will make the DataTransformer
    export capable.
    """
    @tdtaf.export
    def export(a, b, c): # pylint: disable=unused-variable
        pass
    assert tdtaf.is_export_capable() == True
    return


###############################################################################
####                          Test General Settings                        ####
###############################################################################

def test_factory_general_setting(tdtaf):
    """
    Test if the general_setting fucntion can be registerd.
    """
    tdtaf.general_setting('field1', str)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': None
    }
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': None
    }
    return

def test_factory_general_setting_with_default(tdtaf):
    """
    Check the default value is stored correctly.
    """
    tdtaf.general_setting('field1', str, default='value1')
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': 'value1'
    }
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': 'value1'
    }
    return

def test_factory_general_setting_with_ui(tdtaf):
    """
    Check the default value is ui.
    """
    ui_config = {
        'type': 'textbox',
        'label': 'field1',
        'placeholder': 'e.g. value here'
    }
    tdtaf.general_setting('field1', str, ui=ui_config)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': {
                'type': 'textbox',
                'label': 'field1',
                'placeholder': 'e.g. value here'
            }
        }
    }
    assert tdtaf._import_context == {
        'field1': None
    }
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': {
                'type': 'textbox',
                'label': 'field1',
                'placeholder': 'e.g. value here'
            }
        }
    }
    assert tdtaf._export_context == {
        'field1': None
    }
    return


def test_factory_general_setting_conflict_default_config(tdtaf):
    """
    If a key in the default config is set, an error should be raised if there
    is an attempt to create a setting with a name that is in the list of keys.
    """
    tdtaf.set_default_context({
        'field1': 'value1'
    })
    with pytest.raises(ValueError):
        tdtaf.general_setting('field1', str)
    return


def test_factory_general_setting_conflict_import_setting(tdtaf):
    """
    If a field is specified in the import settings then a field with the same
    name is specified in the general settings, an error is raised. This is
    because it is ambiguous as to use the import setting or the general
    setting for the importer.
    """
    tdtaf.import_setting('field1', str)
    with pytest.raises(ValueError):
        tdtaf.general_setting('field1', str)
    return


def test_factory_general_setting_conflict_export_setting(tdtaf):
    """
    If a field is specified in the export settings then a field with the same
    name is specified in the general settings, an error is raised. This is
    because it is ambiguous as to use the export setting or the general
    setting for the exporter.
    """
    tdtaf.export_setting('field1', str)
    with pytest.raises(ValueError):
        tdtaf.general_setting('field1', str)
    return


def test_factory_general_setting_twice(tdtaf):
    """
    Check if two general settings can be specified.
    """
    tdtaf.general_setting('field1', str)
    tdtaf.general_setting('field2', str)
    assert tdtaf._import_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        },
        'field2': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._import_context == {
        'field1': None,
        'field2': None
    }
    assert tdtaf._export_ui_config == {
        'field1': {
            'type': 'str',
            'ui': None
        },
        'field2': {
            'type': 'str',
            'ui': None
        }
    }
    assert tdtaf._export_context == {
        'field1': None,
        'field2': None
    }
    return


def test_factory_general_setting_same_field_name(tdtaf):
    """
    Raise an error if general_settings is used twice with the same field name.
    """
    tdtaf.general_setting('field1', str)
    with pytest.raises(ValueError):
        tdtaf.general_setting('field1', str)
    return


###############################################################################
####                             Test UI Settings                          ####
###############################################################################

def test_factory_default_ui_configs(tdtaf):
    """
    Check that there are no ui configurations on creation.
    """
    assert tdtaf._import_ui_config == {}
    assert tdtaf._export_ui_config == {}
    return


###############################################################################
####                      Test Reprocess Audio Decorators                  ####
###############################################################################

def test_factory_replace_reprocess_audio(tdtaf):
    """
    Test if the replace_reprocess_audio fucntion can be registered.
    """
    @tdtaf.replace_reprocess_audio
    def reprocess(audio_paths, output_dir_path, add_audio, temp_dir):
        pass
    # White-box testing
    assert tdtaf._audio_processing_callback is reprocess
    return


def test_factory_replace_reprocess_audio_twice(tdtaf):
    """
    The replace_reprocess_audio function can only be registered once.
    Registering it twice raises an error.
    """
    @tdtaf.replace_reprocess_audio
    def reprocess1(audio_paths, output_dir_path, add_audio, temp_dir): # pylint: disable=unused-variable
        pass

    with pytest.raises(RuntimeError):
        @tdtaf.replace_reprocess_audio
        def reprocess2(audio_paths, output_dir_path, add_audio, temp_dir): # pylint: disable=unused-variable
            pass
    return


###############################################################################
####                         Test Temp Dir Decorators                      ####
###############################################################################


def test_factory_use_temporary_directory(tdtaf):
    """
    Check if use_temporary_directory is registered.
    """
    # White-box testing
    assert len(tdtaf._functions_using_tempdir) == 0
    @tdtaf.use_temporary_directory
    def f(temp_dir): # pylint: disable=unused-variable
        pass
    assert len(tdtaf._functions_using_tempdir) == 1
    return


def test_factory_use_temporary_directory_twice(tdtaf):
    """
    Check if use_temporary_directory is registered twice.
    """
    # White-box testing
    assert len(tdtaf._functions_using_tempdir) == 0
    @tdtaf.use_temporary_directory
    def f(temp_dir): # pylint: disable=unused-variable
        pass
    @tdtaf.use_temporary_directory
    def g(temp_dir): # pylint: disable=unused-variable
        pass
    assert len(tdtaf._functions_using_tempdir) == 2
    return


def test_factory_double_use_temporary_directory(tdtaf):
    """
    Avoid complecated code by raising an error when nesting temporary
    directories.
    """
    with pytest.raises(RuntimeError):
        @tdtaf.use_temporary_directory
        @tdtaf.use_temporary_directory
        def f(temp_dir): # pylint: disable=unused-variable
            pass
    return


def test_factory_use_temporary_directory_import_files(tdtaf):
    """
    Use use_temporary_directory on import_files.
    """
    @tdtaf.import_files('test')
    @tdtaf.use_temporary_directory
    def f(a, b, c, temp_dir): # pylint: disable=unused-variable
        pass
    return


def test_factory_use_temporary_directory_import_directory(tdtaf):
    """
    Use use_temporary_directory on import_directory.
    """
    @tdtaf.import_directory
    @tdtaf.use_temporary_directory
    def f(a, b, c, temp_dir): # pylint: disable=unused-variable
        pass
    return


def test_factory_use_temporary_directory_export(tdtaf):
    """
    Use use_temporary_directory on export.
    """
    @tdtaf.export
    @tdtaf.use_temporary_directory
    def f(a, b, c, temp_dir): # pylint: disable=unused-variable
        pass
    return


###############################################################################
####                     Test Factory Decorator Attributes                 ####
###############################################################################

def test_factory_attr_name_is_existing_name_import_file():
    """
    Raise an error when a function has the name of an arrtibute in the
    DataTransformer object.
    """
    with pytest.raises(NameError):
        @tdtaf.import_file('.test')
        def __doc__(a,b,c): # pylint: disable=unused-variable
            pass
    return


def test_factory_attr_name_is_existing_name_import_directory():
    """
    Raise an error when a function has the name of an arrtibute in the
    DataTransformer object.
    """
    with pytest.raises(NameError):
        @tdtaf.import_directory
        def __doc__(a,b,c): # pylint: disable=unused-variable
            pass
    return


def test_factory_attr_name_is_existing_name_export():
    """
    Raise an error when a function has the name of an arrtibute in the
    DataTransformer object.
    """
    with pytest.raises(NameError):
        @tdtaf.export
        def __doc__(a,b,c): # pylint: disable=unused-variable
            pass
    return


def test_factory_two_attributes_with_same_name(tdtaf):
    """
    If two functions are defined with the same name then raise an error.
    """
    @tdtaf.import_files('test1')
    def f(a,b,c): # pylint: disable=unused-variable
        pass

    with pytest.raises(NameError):
        @tdtaf.import_files('test2')
        def f(a,b,c): # pylint: disable=function-redefined
            pass
    return


###############################################################################
####                              Test Building                            ####
###############################################################################

from . import make_importer, make_exporter

def test_build_importer(tdtaf, tmpdir):
    """
    Check that the build_importer method constructs a DataTransformer that is
    import capable.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = tdtaf.build_importer(
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda a: None,
    )
    assert type(dt) == DataTransformer
    return


def test_build_exporter(tdtaf, tmpdir):
    """
    Check that the build_exporter method constructs a DataTransformer that is
    export capable.
    """
    @tdtaf.export
    def ex(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = tdtaf.build_exporter(
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None,
    )
    assert type(dt) == DataTransformer
    return


def test_make_importer(tdtaf, tmpdir):
    """
    Use the make_importer function to create an importer data transformer.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = make_importer( # pylint: disable=unused-variable
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )
    assert type(dt) == DataTransformer
    return


def test_make_importer_non_existant(tmpdir):
    """
    Using the make_importer requesting a name that has not been registered will
    raise an error.
    """
    with pytest.raises(ValueError):
        dt = make_importer( # pylint: disable=unused-variable
            '__TEST_DOES_NOT_EXIST',
            str(tmpdir.mkdir('collection')),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    return


def test_make_importer_from_export_only(tdtaf, tmpdir):
    """
    Raise an error if the DataTransformerAbstractFactory associated with the
    name passed to the make_importer function is only capable of being an
    exporter.
    """
    @tdtaf.export
    def ex(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    with pytest.raises(ValueError):
        dt = make_importer( # pylint: disable=unused-variable
            TEST_FACTORY_TDTAF,
            str(tmpdir.mkdir('collection')),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    return


def test_make_exporter_from_import_only(tdtaf, tmpdir):
    """
    Raise an error if the DataTransformerAbstractFactory associated with the
    name passed to the make_exporter function is only capable of being an
    importer.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass
    
    with pytest.raises(ValueError):
        dt = make_exporter( # pylint: disable=unused-variable
            TEST_FACTORY_TDTAF,
            str(tmpdir.mkdir('collection')),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
        # TODO: change arguments for the exporter
    return


def test_make_exporter(tdtaf, tmpdir):
    """
    Use the make_exporter function to create an importer data transformer.
    """
    @tdtaf.export
    def ex(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = make_exporter(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )
    # TODO: change arguments for the exporter
    assert type(dt) == DataTransformer
    return


def test_make_exporter_non_existant(tmpdir):
    """
    Using the make_exporter requesting a name that has not been registered will
    raise an error.
    """
    with pytest.raises(ValueError):
        dt = make_exporter( # pylint: disable=unused-variable
            '__TEST_DOES_NOT_EXIST',
            str(tmpdir.mkdir('collection')),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    # TODO: change arguments for the exporter
    return


###############################################################################
####                      Test DataTransformer (Importer)                  ####
###############################################################################

def test_dt_name(tdtaf, tmpdir):
    """
    Check that the DataTransformer has the name specified.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    assert dt.get_name() == TEST_FACTORY_TDTAF
    assert dt.get_state()['name'] == TEST_FACTORY_TDTAF
    return


def test_dt_get_audio_extention(tdtaf, tmpdir):
    """
    Check that that DataTransformer has the audio extention specified by the
    DataTransformerAbstractFactory.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    assert dt.get_audio_extention() == '.wav'
    return


def test_dt_change_setting_callback(tdtaf, tmpdir):
    """
    When a setting (context) is changed, the callback is triggered and
    notifying external objects of the change.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    tdtaf.general_setting('field', str)

    callback_called = False
    callback_field = None
    
    def callback(ctx):
        callback_called = True        # pylint: disable=unused-variable
        callback_field = ctx['field'] # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        callback
    )

    dt.context['field'] = 'updated_value'

    assert callback_called == True
    assert callback_field == 'updated_value'
    return


def test_dt_import_files_direct_call(tdtaf, tmpdir):
    """
    Check that function decorated with import_files can be called directly by
    name from the DataTransformer object. The only parameter these functions
    accept directly is a list of files.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    file_list = [ str(collection.join(f'file{i}.test')) for i in range(3) ]
    for i in range(3):
        collection.join(f'file{i}.test').write('')

    @tdtaf.import_files('test')
    def import_test_files(paths, ctx, add_anno): # pylint: disable=unused-variable
        assert paths == file_list
        ran_importer = True # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.import_test_files(file_list)
    assert ran_importer == True
    return


def test_dt_import_files_called_by_importer(tdtaf, tmpdir):
    """
    Check that function decorated with import_files can be called indirectly by
    the DataTransformer's process function.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    file_list = [ str(collection.join(f'file{i}.test')) for i in range(3) ]
    for i in range(3):
        collection.join(f'file{i}.test').write('')

    @tdtaf.import_files('test')
    def import_test_files(paths, ctx, add_anno): # pylint: disable=unused-variable
        assert paths == file_list
        ran_importer = True # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.process()
    assert ran_importer == True
    return


def test_dt_import_directory_direct_call(tdtaf, tmpdir):
    """
    Check that the funtion decorated with import_directory can be called
    directly by name from the DataTransformer object. The only parameter these
    functions accept directly is a path to a directory.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    file_set = { f'file{i}.test' for i in range(3) }
    for i in range(3):
        collection.join(f'file{i}.test').write('')

    @tdtaf.import_directory
    def import_test_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        path = Path(path)
        assert { f for f in path.iterdir() } == file_set
        ran_importer = True # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.import_test_dir()
    assert ran_importer == True
    return


def test_dt_import_directory_called_by_importer(tdtaf, tmpdir):
    """
    Check that function decorated with import_directory can be called
    indirectly by the DataTransformer's process function.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    file_set = { f'file{i}.test' for i in range(3) }
    for i in range(3):
        collection.join(f'file{i}.test').write('')

    @tdtaf.import_directory
    def import_test_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        path = Path(path)
        assert { f for f in path.iterdir() } == file_set
        ran_importer = True # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.process()
    assert ran_importer == True
    return


def test_dt_import_only_dirs(tdtaf, tmpdir):
    """
    No files so no import happens. Tries and tricks the importer.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    for i in range(3):
        collection.mkdir(f'file{i}.test')
        # These are directories!

    @tdtaf.import_files('test')
    def import_test_files(path, ctx, add_anno): # pylint: disable=unused-variable
        #should never run
        ran_importer = True # pylint: disable=unused-variable

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.process()
    assert ran_importer == False
    return


def test_dt_import_path_non_existant(tdtaf, tmpdir):
    """
    Raise an error if the import directory given does not exist.
    """

    @tdtaf.import_files('test')
    def import_test_files(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    collection = tmpdir.join('collection')
    with pytest.raises(RuntimeError):
        dt = make_importer(
            TEST_FACTORY_TDTAF,
            str(collection),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    return

def test_dt_import_missing_resampled(tdtaf, tmpdir):
    """
    Raise an error if the resampled directory given does not exist.
    """

    @tdtaf.import_files('test')
    def import_test_files(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    with pytest.raises(RuntimeError):
        dt = make_importer(
            TEST_FACTORY_TDTAF,
            str(tmpdir.mkdir('collection')),
            str(tmpdir.join('resampled')),
            str(tmpdir.mkdir('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    return


def test_dt_import_missing_temporary(tdtaf, tmpdir):
    """
    Raise an error if the temporary directory given does not exist.
    """

    @tdtaf.import_files('test')
    def import_test_files(path, ctx, add_anno): # pylint: disable=unused-variable
        pass

    with pytest.raises(RuntimeError):
        dt = make_importer(
            TEST_FACTORY_TDTAF,
            str(tmpdir.mkdir('collection')),
            str(tmpdir.mkdir('resampled')),
            str(tmpdir.join('temporary')),
            str(tmpdir.join('annotaions.json')),
            lambda ctx: None
        )
    return


def test_dt_import_files_has_context(tdtaf, tmpdir):
    """
    Check that funcitons decorated with import_files gets the correct import
    context.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    collection.join(f'file0.test').write('')

    @tdtaf.import_files('test')
    def import_f(paths, ctx, add_anno): # pylint: disable=unused-variable
        assert 'field' in ctx
        ran_importer = True # pylint: disable=unused-variable

    tdtaf.import_setting('field', str)

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(collection),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    assert dt.context['field'] == None
    dt.process()
    assert ran_importer == True
    return


def test_dt_import_files_add_annotaion(tdtaf, tmpdir):
    """
    Check that annotaions are added when the callback is used.
    """
    ran_importer = False
    collection = tmpdir.mkdir('collection')
    collection.join(f'file0.test').write('')

    @tdtaf.import_files('test')
    def import_test_files(paths, ctx, add_anno): # pylint: disable=unused-variable
        add_anno('some_file', {
            'audio_file_name': 'some_file.wav',
            'transcript': 'la la la',
            'start_ms': 0,
            'stop_ms': 1100
        })
        ran_importer = True

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.join('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.process()
    assert ran_importer == True
    assert 'some_file' in dt._annotation_store
    assert dt._annotation_store['some_file'] == {
            'audio_file_name': 'some_file.wav',
            'transcript': 'la la la',
            'start_ms': 0,
            'stop_ms': 1100
        }
    return


def test_dt_import_directory_has_context(tdtaf, tmpdir):
    """
    Check that funcitons decorated with import_directory gets the correct import
    context.
    """
    ran_importer = False

    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        assert 'field' in ctx
        ran_importer = True # pylint: disable=unused-variable

    tdtaf.import_setting('field', str)

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    assert dt.context['field'] == None
    dt.process()
    assert ran_importer == True
    return


def test_dt_import_directory_add_annotaion(tdtaf, tmpdir):
    """
    Check that annotaions are added when the callback is used.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        add_anno('some_file', {
            'audio_file_name': 'some_file.wav',
            'transcript': 'la la la',
            'start_ms': 0,
            'stop_ms': 1100
        })

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    dt.process()
    assert 'some_file' in dt._annotation_store
    assert dt._annotation_store['some_file'] == {
            'audio_file_name': 'some_file.wav',
            'transcript': 'la la la',
            'start_ms': 0,
            'stop_ms': 1100
        }
    return


def test_dt_add_annotaion_wrong_type(tdtaf, tmpdir):
    """
    Raise an error if the dictionary given to add_annotation contains an
    incorrect field or missing a field.
    """
    @tdtaf.import_directory
    def import_dir(path, ctx, add_anno): # pylint: disable=unused-variable
        add_anno('some_file', {
            'wrong': 'some_file.wav',
            'transcript': 'la la la',
            'start_ms': 0,
            'stop_ms': 1100
        })

    dt = make_importer(
        TEST_FACTORY_TDTAF,
        str(tmpdir.mkdir('collection')),
        str(tmpdir.mkdir('resampled')),
        str(tmpdir.mkdir('temporary')),
        str(tmpdir.join('annotaions.json')),
        lambda ctx: None
    )

    with pytest.raises(RuntimeError):
        dt.process()
    return


###############################################################################
####                      Test DataTransformer (Importer)                  ####
###############################################################################

# def test_dt_export_path_non_existant():
#     """
#     Raise an error if the directory given as the output path does not exist.
#     """
#     pass


# def test_dt_exporter_has_context(tdtaf, tmpdir):
#     """
#     Check that funcitons decorated with export_directory gets the correct export
#     context.
#     """
#     @tdtaf.export
#     def ex(path, ctx, add_anno): # pylint: disable=unused-variable
#         pass

#     tdtaf.export_setting('field', str)

#     dt = make_exporter(
#         TEST_FACTORY_TDTAF,
#         str(tmpdir.join('transcription.ctm')),
#         str(tmpdir.join('audio.wav')),
#         str(tmpdir.mkdir('temporary')),
#         str(tmpdir.join('transcription.ctm')),
#         lambda ctx: None
#     )
#     # TODO: Change arguments above for exporter
    
#     assert dt.context['field'] == None
#     return


# def test_dt_default_audio_resampler():
#     """
#     Check that the default audio resampler produces new audio files.
#     """
#     pass