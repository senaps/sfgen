import argparse
import os
import sys

from distutils.dir_util import copy_tree

TEMPLATES_PATH = os.path.join(os.path.abspath("."), "templates/")


def make_dest(project_path, app_name, app_type):
    """check if the path is okay to write to

    we will check if the path doesnt already exist, and then create the app
    project structure, copying all the files from the templates to it.
    """
    tmp_path = os.path.join(project_path, app_name)
    if os.path.exists(tmp_path):
        raise FileExistsError(f"a file in {tmp_path} already exists.")
    os.mkdir(tmp_path)  # create the project path
    copy_tree(TEMPLATES_PATH + app_type, tmp_path)
    return True


def make_simple_app(app_name, app_path):
    """
    """
    make_dest(app_name=app_name, project_path=app_path, app_type="simple_app")


def make_full_app(app_name, app_path):
    make_dest(app_name=app_name, project_path=app_path, app_type="full_app")


APP_TYPES = {
    "simple": make_simple_app,
    "full": make_full_app
}


if __name__ == "__main__":
    description = "senaps fast [code (flask)] generator"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("app_type", choices=APP_TYPES.keys())
    parser.add_argument("-n", "--name", default="app",
                        help="the name of the app", dest="name")
    parser.add_argument("-p", "--path", default=".", dest="project_path",
                        help="the path to create the app in")
    args = parser.parse_args()
    APP_TYPES[args.app_type](args.name, args.project_path)
