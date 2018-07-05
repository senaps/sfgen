import os

import click
import requests

from zipfile import ZipFile
from io import BytesIO

from .defaults import *

@click.group()
def cli():
    """the command line for senaps Flask Generator

    this application is on it's first phase, and is not complete really.
    senaps.
    """
    pass


@cli.command()
@click.argument('project_type', type=str)
@click.option('-n', '--name', help='the name of the project',
              type=str)
@click.option('-o', '--path', help='the location where the project should be'\
              'created at', default=paths.get('tmp'), type=str)
def create(project_type, name, path):
    """create a new  bare-bone project

    this will receive an argument of `project_type` as first parameter which must
    be provided by the user, and two other parameters for `name` of the project
    and the `path` it should be created at. name and path are optional and if
    are not provided by user, default values will be used instead.

    :param project_type: the type of project to generate ('flask', 'module', etc)
    :param name: the name of the folder that would be created for the project
    :param path: the path to create the project at.
    """
    if project_type not in names:
        click.echo(
            click.style("this project type is not implemented yet, or you have"\
                        "typo in your project type!", fg="red"))
        return
    url = urls.get(project_type)

    try:
        tmpfile = ZipFile(BytesIO(requests.get(url).content))
        tmpfile.extractall(path=path)
        if name:
            current_name = path + names.get(project_type)
            new_name = path + name
            os.rename(current_name, new_name)
    except IOError:
        click.echo(click.style("could not write file to this location",
                               fg="red"))
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


if __name__ == '__main__':
    cli()
