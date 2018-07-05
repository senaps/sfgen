__all__ = ['urls', 'names', 'paths']

import os

# urls are where `sfgen` should look for the project types, these include the
# download links for each project type.
urls = {
    'flask': 'https://github.com/senaps/flask_bare/archive/0.0.1-alpha.zip',
    'module': 'https://github.com/senaps/bare_module/archive/0.0.1-alpha.zip'
    }

# these are the default names to use for the projects, if not specified, one
# of these names would be used.
names = {
    'flask': 'flask_bare-0.0.1-alpha',
    'module': 'bare_module-0.0.1-alpha'
    }


# paths is used for default path's to place the generated project at, with
# `tmp` placing the code to `/tmp/sfgen` folder and current_location placing
# the project into the current working directory.( right where the code is
# being called.
paths = {
    'tmp': '/tmp/sfgen/',
    'current_location': os.path.abspath(os.curdir),
    }