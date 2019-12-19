import argparse
import os
import sys

from distutils.dir_util import copy_tree
from itertools import repeat

APP_TYPES = ['simple', 'full']
TEMPLATES_PATH = os.path.join(os.path.abspath("."), "templates/")


def make_path(project_path, app_name):
    return os.path.join(project_path, app_name) + "/"


def make_dest(project_path, app_name, app_type):
    """check if the path is okay to write to

    we will check if the path doesnt already exist, and then create the app
    project structure, copying all the files from the templates to it.
    """
    tmp_path = make_path(project_path, app_name)
    if os.path.exists(tmp_path):
        raise FileExistsError(f"a file in {tmp_path} already exists.")
    os.mkdir(tmp_path)  # create the project path
    copy_tree(TEMPLATES_PATH + app_type, tmp_path)
    return tmp_path


def get_files(directory, app_name):
    for root, folders, files in os.walk(directory):
        for file_obj in files:
            if file_obj.endswith("tmpl"):
                fix_template(project_name=app_name, file_path=file_obj)
                fix_filename(name=file_obj, file_path=directory,
                             project_name=app_name)
    return templates, names


def fix_filename(name, file_path, project_name):
    file_end = "." + name.split(".")[-1]
    os.rename(file_path + name, file_path + project_name + file_end)


def fix_template(project_name, file_path):
    pass


def make_app(app_name, app_path, app_type):
    """
    """
    app_type = app_type + "_app"
    dest = make_dest(app_name=app_name, project_path=app_path, app_type=app_type)
    directory = make_path(app_name=app_name, project_path=app_path)
    get_files(directory=dest, app_name=app_name)


if __name__ == "__main__":
    description = "senaps fast [code (flask)] generator"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("app_type", choices=APP_TYPES)
    parser.add_argument("-n", "--name", default="app",
                        help="the name of the app", dest="name")
    parser.add_argument("-p", "--path", default=".", dest="project_path",
                        help="the path to create the app in")
    args = parser.parse_args()
    make_app(args.name, args.project_path, args.app_type)

