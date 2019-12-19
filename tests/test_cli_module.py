import os
import tempfile
import shutil

from contextlib import contextmanager

import pytest

from sfgen.cli import make_path, make_dest


@contextmanager
def make_tmpdir():
    try:
        t = tempfile.mkdtemp()
        yield t
    finally:
        shutil.rmtree(t)


def test_make_path_strings():
    assert make_path("/tmp/", "test") == "/tmp/test/"


def test_make_path_none():
    assert make_path("/tmp/", "something/") == "/tmp/something/"


def test_make_dest_path_exists():
    with make_tmpdir() as tmp:
        os.system(f"mkdir {tmp}/tester")
        with pytest.raises(FileExistsError):
            make_dest(project_path=tmp, app_name="tester",
                      app_type="simple_app")


def test_make_dest(mocker):

    with make_tmpdir() as tmp:
        assert make_dest(project_path=tmp, app_name="tester",
                    app_type="simple_app") == f"{tmp}/tester/"