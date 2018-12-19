import os
import tempfile

import pytest

import elpis

@pytest.fixture
def client():
    elpis.server.config['TESTING'] = True
    client = elpis.server.test_client()

    yield client

def test_empty_page(client):
    """Start with a blank page."""

    rv = client.get('/')
    assert b'Welcome to Elpis' in rv.data