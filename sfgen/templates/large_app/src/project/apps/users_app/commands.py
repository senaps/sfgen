import sys

import click
from sqlalchemy.exc import OperationalError

from . import auth
from .models import Role, User, db
from project.apps.utils import get_app_context


@click.group('user')
def auth_cli():
    """
    cli for managing users
    """


@auth_cli.command('add_role')
@click.argument("name")
@click.option("--production/--development", default=False,
              help="run under prodcution or development configs, default to "\
                   "`development`")
def add_role(name, production):
    """add a new role to the system

    we will receive a new role from the user and then try to add it to the
    system. we will return True if the role already exists in the db.

    :return: True/False fot the role being added to the system
    """
    config = 'production' if production else 'development'
    try:
        with get_app_context(conf=config):
            role_obj = Role.query.filter_by(name=name).first()
            if role_obj:
                click.echo(f"role `{name}` already exists in the system")
                return True
            role = Role(name=name)
            db.session.add(role)
            db.session.commit()
        click.echo(f"role `{name}` was added successfully")
        return True
    except OperationalError:
        click.echo("no db was found. you should init-db first")
    except Exception as e:
        click.echo(str(e))
        raise


@auth_cli.command('add_user')
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument("role")
@click.option("--production/--development", default=False,
              help="run under prodcution or development configs, default to "\
                   "`development`")
def add_user(username, password, email, role, production):
    """add a new user to the db

    receive arguments needed for adding a new user and then, add the given user
    to the db. we will return propper messaging if the username already exists
    in the db.

    :param username: username to be added.
    :param password: password being used for the user.
    :param email: email for the given user.
    :param role: role of the user in the system.
    :return: wheather or not the user is been created.
    """
    config = 'production' if production else 'development'
    try:
        with get_app_context(conf=config):
            user = User.query.filter_by(username=username).first()
            role_obj = Role.query.filter_by(name=role).first()
        if user:
            click.echo(f"user with username `{username}` already exists")
            sys.exit(1)
        if not role_obj:
            click.echo(f"role with name `{role}` doesn't exist. add_role first")
            sys.exit(1)
        with get_app_context(config):
            user = User()
            user.username = username
            user.email = email
            user.password = password
            user.force_password_change = False
            user.role_id = role_obj.id
            db.session.add(user)
            db.session.commit()
        click.echo("done!")
    except OperationalError:
        click.echo("no db was found. you should init-db first")
    except Exception as e:
        click.echo(str(e))
        raise
