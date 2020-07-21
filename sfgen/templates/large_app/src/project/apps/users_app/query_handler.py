"""query handler module

this module is utilized to query the db. whether it' a raw query or a model query.

    - get_user_by_name()  get a user object by their username
    - get_role_by_name()  get a role object by it's name
    - get_authority_by_name()  get an authority by it's name
    - list_roles()  return the list of roles on the system
    - list_users()  return the list of users on the system
    - create_user()  add a new user to the system
"""
from sqlalchemy.exc import IntegrityError

from . import db
from .models import User, Role, Authority, UserAuths
from .messages import *


def get_user_by_name(username: str) -> User:
    """get a user object by their username

    receive a username and return the user object  with the given name or
    `None` if there is no user with that username.

    :arg username: username we want to search the db for
    :return: the user object or None if not found the user
    """
    return User.query.filter_by(username=username).first()


def get_role_by_name(name: str) -> Role:
    """get a role object by it's name

    :param name: name of the role we want to match
    :return: role object or None
    """
    return Role.query.filter_by(name=name).first()


def list_roles(page: int=1, weight=20) -> list:
    """return the list of roles on the system

    this function will query the db for the roles and returns the data
    in pagination.
    the page and weight set the page and rows per page in the system.

    :param page: page of the data
    :param weight: weight of page

    """
    try:
        return Role.query.paginate(page=page, per_page=weight, error_out=False)
    except Exception as e:
        raise


def list_users(query=None, creator_id=None, page=1, weight=20) -> list:
    """return the list of users on the system

    this functon will query the db for users and tries to return a paginated
    result on top of it.
    page and weight represent the page and rows per page of the result

    :param query: query to be executed on the table
    :param page: number of the page to be shown
    :param weight: rows per page to be shown
    :returns: paginated object result
    """
    try:
        q  = User.query
        if query:
            q = q.filter_by(username=query)
        if creator_id:
            q = q.filter((User.id==creator_id)|(User.creator_id==creator_id))
        return q.paginate(page=page, per_page=weight, error_out=False)
    except Exception as e:
        raise


def create_user(username, password, email, role, name=None, family=None, creator=None):
    """add a new user to the system

    this function will receive all the needed variables and will create a new
    user with provided information.

    """
    try:
        user = User()
        user.username = username
        user.role_id = role
        user.password = password
        user.first_name = name
        user.last_name = family
        user.email = email
        user.creator=creator
        db.session.add(user)
        db.session.commit()
        return True
    except IntegrityError:
        raise ValueError("مقدار تکراری است")
    except:
        raise
