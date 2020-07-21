"""app testing client initializer

this module is used to create and load from the fixtures that we may be needing
for testing purposes.

    - client()  a flask testing client instance

"""
import os
import pytest

from project.apps.utils import make_app, get_app_context
from project.extensions import db


@pytest.fixture
def client():
    """flask testing client instance

    this function will try to create a db, return a testing client fixture.
    this function is called before every test and the lines after `yield` are
    being ran after the test.
    so we use this fixture as a setup and cleanup functionality for our tests.

    :return:
    """
    uri = "/tmp/testing-db.db"
    app = make_app(conf="testing")
    with get_app_context('testing'):
        db.create_all()
    yield app.test_client()
    os.remove(uri)
