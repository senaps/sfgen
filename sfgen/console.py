import os

import click
import requests

from zipfile import ZipFile
from io import BytesIO

FLASK_BARE = 'https://github.com/senaps/flask_bare/archive/0.0.1-alpha.zip'
dirname = 'flask_bare-0.0.1-alpha'

@click.group()
def cli():
    """the command line for senaps Flask Generator

    this application is on it's first phase, and is not complete really.
    senaps.
    """
    pass


@cli.command()
@click.option('-n', '--name', help='the name of the project',
              default='test', type=str)
def create_app(name):
    """create a new flask project

    takes in options, currently `name` and creates a new flask project
    based on that.
    TODO: this should take path, check the path and rename the file in
    the given path
    TODO: better exception handeling.
    """
    try:
        tmpfile = ZipFile(BytesIO(requests.get(FLASK_BARE).content))
        tmpfile.extractall()
        os.rename(dirname, name)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


if __name__ == '__main__':
    cli()
