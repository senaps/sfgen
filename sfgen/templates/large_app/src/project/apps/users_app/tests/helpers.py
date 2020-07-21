import random
import string
from dataclasses import dataclass

from flask_jwt_extended import create_access_token

from project.apps.utils import make_app, get_app_context
from ..models import User, Role, Authority, UserAuths
from .. import db


def create_name(n=5):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def make_mail(email=None):
    if not email:
        email = create_name()
    return f"{email}@example.com"


def create_user(username="admin", password="admin", env=None, **kwargs):
    email = kwargs.get("email", make_mail())
    password_change = kwargs.get("password_change", False)
    role = kwargs.get("role", 1)
    with get_app_context(conf='testing'):
        if not 'no_role' in kwargs.keys():
            role2= Role(id=2,name="Administrator")
            role3= Role(id=3,name="Reporter")
            db.session.add(role1)
            db.session.add(role2)
            db.session.add(role3)
            db.session.commit()
        user = User()
        user.username = username
        user.email = email
        user.password=password
        user.force_password_change = password_change
        user.role_id = role
        if 'creator' in kwargs.keys():
            user.creator_id = kwargs.get("creator")
        db.session.add(user)
        db.session.commit()


def get_access_token_header(username=None):
    """get an auth token

    create a fake access token and then put it in the header object
    to be passed
    to the routes. this object assumes the user exists in the db.
    **Note: this is not testing the login functionality

    :param username: username to whom access token is created
    :return: header dict containing token for access to routes with auth
    """
    if not username:
        create_user(username="admin", password="admin")
        username = "admin"
    with get_app_context('testing'):
        token = create_access_token(identity=username)
    return {'Authorization': f'Bearer {token}'}