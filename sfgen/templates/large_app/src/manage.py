"""manage the application

this module will allow for easy command's utilizations for the app. we use `click`
for command creation. helping with running and testing the app and so much more

    - do_initdb()  create the db using the provided configs
    -

"""
import os
import sys

import click

from project.application import create_app
from project.config import CONFIG_MAPPER
from project.extensions import db

from project.apps.users_app.commands import auth_cli


deploy = os.environ.get('FLASK_ENV', 'development')
app = create_app(CONFIG_MAPPER.get(deploy))


def do_initdb(application=None):
    if not application:
        global app
    else:
        app = application
    try:
        with app.app_context():
            db.create_all()
            click.echo("db is initialized")
    except Exception as e:
        click.echo(str(e))

@click.group()
def cli():
    """Management script for web console application"""


@cli.command()
def initdb():
    """
    create the db with tables and stuff we need to be initialized
    """
    do_initdb()

cli.add_command(auth_cli)

if __name__ == '__main__':
    cli()