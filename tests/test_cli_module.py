import os
import tempfile
import shutil

from contextlib import contextmanager

import pytest

from sfgen.cli import make_path, make_dest, get_file_content, set_file_content


def test_make_path_strings():
    assert make_path("/tmp/", "test") == "/tmp/test/"


def test_make_path_with_traling_slash():
    assert make_path("/tmp/", "something/") == "/tmp/something/"


def test_make_dest_path_exists():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir.split("/")
        with pytest.raises(FileExistsError):
            make_dest(project_path="/tmp", app_name=file_name[-1],
                      app_type="simple_app")


def test_make_dest(mocker):
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert make_dest(project_path=tmp_dir, app_name="tester",
                    app_type="simple_app") == f"{tmp_dir}/tester/"


def test_get_file_read_data():
    with tempfile.NamedTemporaryFile(mode="w") as tmp_file:
        tmp_file.write("hello world!")
        tmp_file.seek(0)
        assert get_file_content(tmp_file.name) == "hello world!"


def test_set_file_content():
    with tempfile.NamedTemporaryFile() as temp_file:
        set_file_content(temp_file.name, "hello world!")
        assert temp_file.read() == b"hello world!"