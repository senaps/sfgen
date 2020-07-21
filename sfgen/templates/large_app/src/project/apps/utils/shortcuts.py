"""shortcuts to variables or functions we may need in other packages

using this module's functionality, we will be able to centeralize the structure
of the configs so every application is importing from the same place not
looking for functionality and api all around the project.

    - get_app_context()    get an app context
    - make_app()  create an app
"""
import os
from contextlib import contextmanager

from project.application import create_app
from project.config import CONFIG_MAPPER as cm


@contextmanager
def get_app_context(conf=None):
    """get an app context!

    we will receive the name of the application and then try to build out the
    applicaton and return it. the important thing with this function is that we
    will return the application context not the actual application object.
    this is usefull for modules and functions that need the application context
    to be able to do what they would need to do.

    the config is the name of the config class we want to use to create the app
    with.

    :param conf: name of the config class
    :return: a flask application context
    """
    if not conf:
        conf = 'development'
    try:
        app = create_app(cm.get(conf))
        with app.app_context() as ctx:
            yield ctx
    finally:
        pass


def make_app(conf=None):
    """create and return an app object

    this function will create an application object and return it's instance. this
    could be used to create test client for testing or making deploy application
    and etc. though a user can just create an app and be fine with it, we are
    exposing this fucntion so the user is able to easily create applications
    without getting involved with importing different modules and functions from
    different files

    :param conf: name of the configuration to build the app with
    :return: application object
    """
    if not conf:
        conf = 'development'
    app = create_app(cm.get(conf))
    return app