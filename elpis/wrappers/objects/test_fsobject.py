import pytest, re
from pathlib import Path
from .fsobject import FSObject


def test_base_class_creation(tmpdir):
    """
    Creation of a base class without being inherited must fail.
    """
    with pytest.raises(TypeError):
        obj = FSObject()
    return


class Example(FSObject):
    # same arguments as base class
    def __init__(self,
                 parent_path: str = None,
                 dir_name: str = None, # Optional
                 name: str = None,
                 pre_allocated_hash: str = None # Optional
                 ):
        super().__init__(parent_path, dir_name, name, pre_allocated_hash)


def test_missing_config_file_var(tmpdir):
    """
    Creation of an object without _config_file class variable.

    An instance of FSObject must have the class attribute `self._config_file`
    which points to the file containing the objects persistant variables.
    """
    # Black-box
    class A(FSObject):
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}
    with pytest.raises(TypeError):
        A(parent_path=tmpdir, name='a')
    return


def test_missing_state_property(tmpdir):
    """
    Creation of an object without _config_file class variable.

    An instance of FSObject must have the class attribute `self._config_file`
    which points to the file containing the objects persistant variables.
    """
    # Black-box
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
    with pytest.raises(TypeError):
        A(parent_path=tmpdir, name='a')
    return


def test_invalid_config_file_type(tmpdir):
    """
    _config_file must be a JSON file, so must have extension '.json'
    """
    # Black-box
    class A(FSObject):
        _config_file = 'a'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}
    with pytest.raises(ValueError):
        a = A(parent_path=tmpdir, name='a')
    return


def test_no_optional_args(tmpdir):
    """
    Check that state of an object when minimal variables are assigned.
    """
    # White-box
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}

    A(parent_path=tmpdir, name='a')
    # No exceptions should occure
    return


def test_dir_name(tmpdir):
    """
    Check that state of an object when minimal variables are assigned.
    """
    # White-box
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}

    a = A(parent_path=tmpdir, name='a', dir_name='a_dir')

    assert a.path.exists() # a.path is not hashed
    files = [path.name for path in a.path.iterdir()]
    assert files == ['a.json']
    assert f'{a.path}' == f'{tmpdir}/a_dir'
    return

def test_pre_allocated_hash(tmpdir):
    """
    Check that state of an object when minimal variables are assigned.
    """
    # White-box
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}

    a = A(parent_path=tmpdir, name='a', pre_allocated_hash='a0b1c2d3')

    assert a.path.exists() # a.path is hashed
    files = [path.name for path in a.path.iterdir()]
    assert files == ['a.json']
    assert f'{a.path}' == f'{tmpdir}/a0b1c2d3'


def test_loading(tmpdir):
    """
    Load an object.
    """
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}
        @classmethod
        def load(cls, base_path: Path):
            self = super().load(base_path)
            return self

    a = A(parent_path=tmpdir, name='a')

    b = A.load(f'{tmpdir}/{a.hash}')
    assert b.name == 'a'
    assert b.hash == a.hash
    assert b.date == a.date


def test_protected_variables(tmpdir):
    """
    Test that an error is raised when writing to the variables:
        name
        date
        hash
        path
    """
    class A(FSObject):
        _config_file = 'a.json'
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        @property
        def state(self) -> dict:
            return {}
        @classmethod
        def load(cls, base_path: Path):
            self = super().load(base_path)
            return self

    a = A(parent_path=tmpdir, name='a')
    with pytest.raises(AttributeError):
        a.name = "Name"
    with pytest.raises(AttributeError):
        a.date = "1.1"
    with pytest.raises(AttributeError):
        a.hash = "abcd1234"
    with pytest.raises(AttributeError):
        a.path = "/"
    with pytest.raises(AttributeError):
        a.state = {}
        