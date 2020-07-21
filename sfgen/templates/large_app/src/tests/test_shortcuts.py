from flask import Flask

from project.apps.utils.shortcuts import make_app


def test_make_app():
    assert isinstance(make_app(), Flask)


def test_develop_passed_config():
    app = make_app(conf="development")
    assert app.config['SECRET_KEY'] == "testmy app"


def test_develop_empty_config():
    app = make_app()
    assert app.config['SECRET_KEY'] == "testmy app"

def test_develop_non_existing_config():
    app = make_app(conf="doesntexist")
    assert app.config.get('SECRET_KEY') == None and isinstance(app, Flask)
