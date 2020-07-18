"""sfgen [Senaps Fast application generator!]

this code is going to allow me to quickly launch a new boilerplate application
I have setup some applications like a simple flask app, full blueprint based
flask app and etc.

we want to use as few out of standard library packages as possible :)

functions in this module are:

    - make_path()  make the path string for the application
    - make_dest()  check if the path is okay to write to
    - get_file_content()  open a file and return it's content
    - set_file_content()  write the received content to the file
    - get_files()  check project files and fix their name and data
    - fix_filename()  remove the .tmpl from the name of the file
    - fix_template()  replace the variables in the file with actual text
    - make_app()  make an application
"""
import argparse
import os
import sys

from distutils.dir_util import copy_tree
from string import Template


APP_TYPES = ['simple', 'full']

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_PATH = os.path.join(BASE_DIR, "sfgen/templates/")


def make_path(project_path, app_name):
    """make the path string for the application

    this will receive the `path` and the `app_name` and will join the two to
    create the path.

    :param project_path: the path to create the app
    :param app_name: the name of folder to be created
    :return: the path str
    """
    if app_name.endswith("/"):
        app_name = app_name[:-1]
    return os.path.join(project_path, app_name) + "/"


def make_dest(project_path, app_name, app_type):
    """check if the path is okay to write to

    we will check if the path doesnt already exist, and then create the app
    project structure, copying all the files from the templates to it.

    :param project_path: path to create the project folder
    :param app_name: the name of the application/folder to be created
    :param app_type: the type of the application template
    """
    tmp_path = make_path(project_path, app_name)
    if os.path.exists(tmp_path):
        raise FileExistsError(f"a file in {tmp_path} already exists.")
    os.mkdir(tmp_path)  # create the project path
    copy_tree(TEMPLATES_PATH + app_type, tmp_path)  # what if template doesnt exist?
    return tmp_path


def get_file_content(file_path):
    """open a file and return it's content

    :param file_path: the path of the file
    :return: string of the file
    """
    with open(file_path, "r") as tmp:
        return tmp.read()


def set_file_content(file_path, content):
    """write the received content to the file

    :param file_path: the path to write to
    :param content: the content to be written to the file
    :return:
    """
    with open(file_path, "w") as tmp:
        tmp.write(content)


def get_files(directory, app_name):
    """check project files and fix their name and data

    this function will loop over the whole files copied to the destination and
    if any of those files is ended with a `.tmpl` filename, will try to edit
    the content and the name of it.

    :param directory: the path we have pasted the application to
    :param app_name: the name of the application
    :return:
    """
    for root, folders, files in os.walk(directory):
        for file_obj in files:
            if file_obj.endswith("tmpl"):
                fix_template(project_name=app_name, file_path=directory,
                             name=file_obj)  # fix the content
                fix_filename(name=file_obj, file_path=directory,
                             project_name=app_name)  # fix the name


def fix_filename(name, file_path, project_name):
    """remove the .tmpl from the name of the file

    this function will receive a filename and will try to fix it's name by
    removing the `.tmpl` from it's name.

    :param name: name of the file
    :param file_path: path which the file is at
    :param project_name: the name of the project?
    :return:
    """
    if name.endswith(".tmpl"):
        new_name = name[:-5]
    os.rename(file_path + name, file_path + new_name)



def fix_template(name, file_path, project_name):
    """replace the variables in the file with actual text

    this function will receive the path and name of a file and will open it,
    render it's data and will write the content back to it.
    we will use the Template render methods from the python standard library
    for this functionality.

    :param name: name of the file to be fixed
    :param file_path: path of the file
    :param project_name: name of the project to be replaced
    :return:
    """
    tmp_path = file_path + name
    text = get_file_content(file_path=tmp_path)
    res = Template(text).substitute(project_name=project_name)
    set_file_content(file_path=tmp_path, content=res)


def make_app(app_name, app_path, app_type):
    """make an application

    this will receive the `app_type`, `path` to the app and the name of the app
    and will try to create the given application in the path.

    :param app_name: name of the application
    :param app_path: the path to create the app in
    :param app_type: the type of application to be created
    """
    app_type = app_type + "_app"
    try:
        dest = make_dest(app_name=app_name, project_path=app_path,
                         app_type=app_type)
        get_files(directory=dest, app_name=app_name)
    except FileExistsError:
        print("Error: project with this name already exists")


def main():
    description = "senaps fast [code (flask)] generator"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("app_type", choices=APP_TYPES)
    parser.add_argument("-n", "--name", default="app",
                        help="the name of the app", dest="name")
    parser.add_argument("-p", "--path", default=".", dest="project_path",
                        help="the path to create the app in")
    args = parser.parse_args()
    make_app(args.name, args.project_path, args.app_type)


if __name__ == "__main__":
    main()

