import argparse
import os
import sys


def make_simple_app(app_name, app_path):
    pass


def make_full_app(app_name, app_path):
    pass


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
    APP_TYPES[args.app_type](name, project_path)
