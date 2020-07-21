"""views for the user's app

this module contains the functionality needed for handling the users views.
login, logout, register, change_password and all other types of functionality
that we might need to handle in the system.
we are not going to run or write any queries in this module and all of that
should be handled using `query_handler` module functionality.

    - login()  check if the user can login in the system
"""
from flask import request, jsonify, current_app, url_for, abort
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt,
                                get_jwt_identity)
from sqlalchemy.exc import OperationalError
from flasgger import swag_from

from . import auth
from .authentication import blacklist
from .models import db
from .decorators import login_required, admin_required
from .query_handler import (get_user_by_name, get_role_by_name , list_roles,
                            list_users, create_user)
from .utils import check_email, check_user_exists
from ..utils.responses import make_response, make_pagination
from ..utils.status_codes import *
from .messages import *


@auth.route('/login/', methods=['POST'])
@swag_from("swagger_docs/login.yml")
def login():
    """login route

    this function will control the login funcionality of the system.
    we will check for the password and username and if everything is right, we
    will login the user.
    there is an option controling whether the user needs to change their
    password or not, and if so, we will redirect them to another page which
    gives them the login capabilities.
    :return: api token for the user
    """
    data = request.get_json()
    try:
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            #username or password missing!
            data = {"msg": USERNAME_PASSWORD_MISSING}
            return make_response(data=data, status_code=BAD_PARAMETER)
        user = get_user_by_name(username)
        if not user:
            # username was incorrect
            data = {"msg": WRONG_USERNAME_PASSWORD}
            return make_response(data=data, status_code=WRONG_DATA)
        if not user.verify_password(password):
            #password was incorrect!
            data = {"msg": WRONG_USERNAME_PASSWORD}
            return make_response(data=data, status_code=WRONG_DATA)
        access_token = create_access_token(identity=username)
        data = {"access_token": access_token}
        if user.force_password_change:
            data = {"msg": CHANGE_PASSWORD_REQUIRED,
                    "commands": ["redirect"], "access_token": access_token}
            return make_response(data=data, status_code=NOT_ALLOWED)
        data["msg"] = LOGIN_SUCCESSFUL
        return make_response(data=data)
    except OperationalError as e:
        abort(500, "error in db")
    except Exception as e:
        abort(500, "error in server")


@auth.route('/logout/', methods=['DELETE'])
@login_required
@swag_from("swagger_docs/logout.yml")
def logout():
    """logout the user
    this route will remove the token from valids list
    """
    try:
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        data = {"msg": LOGOUT_SUCCESSFUL,
                  "commands": ['logout']}
        return make_response(status_code=OK, data=data)
    except Exception as e:
        abort(500, "server error")


@auth.route('/users/')
@auth.route('/users/<int:page>/', endpoint="userlist_page")
@auth.route('/users/<int:page>/<int:weight>/', endpoint="userlist_full")
@login_required
@swag_from("swagger_docs/userlist.yml")
def user_list(page=1, weight=20):
    """list the users on the system

    we will check for the user's role, if they are not an admin, then they
    just can't see what other users are on the system. admins on the other
    hand are okay and are able to see the full list of users. though they
    can't see the `admin` user. so `admin` user is hidden for every user
    on the system. so that they can't edit this user.

    :param page:
    :param weight:
    :return:
    """
    try:
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        current_user_role = current_user.get_role()
        is_admin = True if current_user_role == "Administrator" else False
        if not is_admin:
            # they only see themselves
            users = list_users(query=current_user_name, page=page, weight=weight)
        elif current_user.username == "admin":
            users = list_users(page=page, weight=weight)
        else:
            users = list_users(page=page, weight=weight,
                               creator_id=current_user.id)
        data_list = list()
        for user in users.items:
            if user.username == "admin" and not current_user_name == "admin":
                #if they are not administrator, they wont see it's user
                continue
            obj = {'username': user.username,
                   'email': user.email,
                   'first_name': user.first_name,
                   'last_name': user.last_name,
                   'role': user.get_role()}
            data_list.append(obj)
        data = make_pagination(data=users)
        data['data'] = data_list
        return make_response(data=data)
    except OperationalError:
        header = {"msg": "db problem"}
        abort(500, header)
    except Exception as e:
        raise
        header = {"msg": "server problem"}
        abort(500, header)


@auth.route('/users/<username>/')
@login_required
@swag_from("swagger_docs/userlist.yml")
def user_details_route(username):
    """return deatils on a given user

    :return:
    """
    try:
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        current_user_role = current_user.get_role()
        is_admin = True if current_user_role == "Administrator" else False
        if not is_admin and current_user_role != "Super":
            data = {"msg": ADMINS_ONLY}
            return make_response(status_code=NOT_ALLOWED, data=data)
        if username == "admin" and current_user.username != "admin":
            data = {"msg": INSUFFICIENT_CREDENTIALS}
            return make_response(status_code= NOT_ALLOWED,
                                 data=data)
        user = get_user_by_name(username)
        if not user:
            data = {"msg": NO_USER_FOUND}
            return make_response(status_code=BAD_PARAMETER,
                                 data=data)
        obj = {'username': user.username,
               'email': user.email,
               'first_name': user.first_name,
               'last_name': user.last_name,
               'role': user.get_role()}
        return make_response(data=obj)
    except OperationalError:
        header = {"msg": "db problem"}
        abort(500, header)
    except Exception as e:
        header = {"msg": "server problem"}
        abort(500, header)



@auth.route('/users/', methods=["POST"])
@admin_required
@swag_from("swagger_docs/create_user.yml")
def register_user():
    """register a new user in the system

    this view will receive the data on a user and will try to register the
    user in the system. we will check for some variables like:
        - username, password, email and role are sent
        - password and confirm password are match
        - if role is valid
        - if username already exists in the db
        - if email is valid?
    and then we will create the user objcet and add them to the db.

    :return: 201 object created or one of the errors
    """
    data = request.get_json()
    username = data.get('username', None)
    role_name = data.get('role', None)
    password = data.get('password', None)
    confirm_pass = data.get('confirm_password', None)
    firstname = data.get('first_name', None)
    lastname = data.get('last_name', None)
    email = data.get('email', None)
    try:
        if (not username) or (not password) or (not email) or (not role_name):
            data = {"msg": REQUIRED_FIELD_MISSING}
            return make_response(data=data, status_code=BAD_PARAMETER)
        if not password == confirm_pass:
            data = {"msg": PASSWORD_MISSMATCH}
            return make_response(status_code=BAD_PARAMETER, data=data)
        role = get_role_by_name(role_name)
        if not role:
            data = {"msg": ROLE_MISSMATCH}
            return make_response(status_code=BAD_PARAMETER, data=data)
        user_exists = check_user_exists(username)
        if user_exists:
            data = {"msg": USERNAME_ALREADY_EXISTS}
            return make_response(status_code=CONFLICT, data=data)
        if not check_email(email):
            data = {"msg": EMAIL_MISSMATCH}
            return make_response(status_code=BAD_PARAMETER, data=data)
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        create_user(username=username, password=password, email=email,
                    role=role.id, name=firstname, family=lastname,
                    creator=current_user)
        data = {"msg": USER_CREATED}
        return make_response(status_code=INSERTED, data=data)
    except ValueError as e:
        data = {"msg": str(e)}
        abort(400, data)
    except OperationalError:
        header = {"msg": "db problem"}
        abort(500, header)
    except Exception as e:
        raise
        header = {"msg": "server problem"}
        abort(500, header)


@auth.route('/users/<username>/', methods=['DELETE'])
@admin_required
@swag_from("swagger_docs/remove_user.yml")
def remove_user(username):
    """remove a user from the users

    we will receive a username and after doing some checks, try to remove the
    user from the database. we will check for
        - if user requesting to remove, is admin
        - if username exists in the db
        - if they want to remove themselves
        - if they want to remove the administrator user
        - if administrator want's to delete it's user

    :return:
    """
    try:
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        user = get_user_by_name(username)
        if not user:
            data = {"msg": EMPTY_DATABASE}
            return make_response(status_code=NO_CONTENT,
                                 data=data)
        if username == "admin":
            data = {"msg": INSUFFICIENT_CREDENTIALS}
            return make_response(status_code=NOT_ALLOWED,
                                 data=data)
        db.session.delete(user)
        db.session.commit()
        data = {"msg": USER_REMOVED}
        return make_response(data=data, status_code=OK)
    except OperationalError:
        header = {"msg": "db problem"}
        abort(500, header)
    except Exception as e:
        raise
        header = {"msg": "server problem"}
        abort(500, header)

#TODO: use a DRY method of serializing the user
@auth.route('/users/<username>/', methods=["PUT"])
@login_required
@swag_from("swagger_docs/edit_user.yml")
def edit_user(username):
    """edit the given user, with provided data

    we will receive some data for a username, and try to update their data
    with this method.
    there are multiple checks and tricks in place prior to editing the user
    in the db:
        - if the user exists in the database
        - if user withouth admin privileges edits another user
        - admin tries to edit administrator
    we will check some other rules too...
        - if new password maches old password
        - if password and confirm password are not identical
        - if role name is valid
        , etc...

    :return:
    """
    data = request.get_json()
    role_name = data.get('role')
    current_password = data.get('current_password')
    password = data.get('password')
    confirm_pass = data.get('confirm_password')
    firstname = data.get('first_name')
    lastname = data.get('last_name')
    email = data.get('email')
    try:
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        current_user_role = current_user.get_role()
        if role_name == current_user_role:
            role_name = None
        is_admin = True if current_user_role in ["Administrator", "Super"] else False
        user = get_user_by_name(username)
        if not user:
            data = {"msg": NO_USER_FOUND}
            return make_response(status_code=BAD_PARAMETER,
                                 data=data)
        self_edit = True if user.username == current_user_name else False
        if  (not self_edit) and (not is_admin) and current_user_role != "Super":
            #user tries to edit someone else!
            data = {"msg": ADMINS_ONLY}
            return make_response(status_code=NOT_ALLOWED, data=data)
        if user.username == "admin" and current_user_name != "admin":
            # normal user editing administrator!
            data = {"msg": INSUFFICIENT_CREDENTIALS}
            return make_response(status_code= NOT_ALLOWED,
                                 data=data)
        if role_name:
            # change the role
            if not is_admin:
                # they are not admins!
                data = {"msg": ADMINS_ONLY}
                return make_response(data=data,
                                     status_code=NOT_ALLOWED)
            if self_edit:
                # they can't change their own role
                data = {"msg": SOMEONE_ELSE_DO_IT}
                return make_response(data=data, status_code=NOT_ALLOWED)
            role = get_role_by_name(role_name)
            if not role:
                # is the role name valid?
                data = {"msg": ROLE_MISSMATCH}
                return make_response(data=data, status_code=BAD_PARAMETER)
            user.role_id = role.id
        if password:
            #change password stuff
            if password != confirm_pass:
                # password and confirm password don't match!
                data = {"msg": PASSWORD_MISSMATCH}
                return make_response(status_code=BAD_PARAMETER, data=data)
            if self_edit and (not user.verify_password(current_password)):
                # if they are editing themselves, current password needed!
                data = {"msg": WRONG_OLD_PASSWORD}
                return make_response(data=data, status_code=BAD_PARAMETER)
            if user.verify_password(password):
                #old password is being used!:)
                data = {"msg": SAME_OLD_NEW_PASSWORD}
                return make_response(data=data, status_code=BAD_PARAMETER)
            # every check passed, change password!:)
            user.password = password
            if user.force_password_change:
                user.force_password_change = False
        if firstname and firstname != user.first_name:
            user.first_name = firstname
        if lastname and lastname != user.last_name:
            user.last_name = lastname
        if email and email != user.email:
            if check_email(email=email):
                user.email = email
            else:
                data = {"msg": EMAIL_MISSMATCH}
                return make_response(data=data, status_code=BAD_PARAMETER)
        db.session.commit()
        return make_response(status_code=INSERTED)
    except OperationalError:
        abort(500, "db problem")
    except Exception as e:
        raise
        abort(500, "server problem")


@auth.route("/users/me/")
@login_required
@swag_from("swagger_docs/user_detail.yml")
def current_user_detail():
    """return the detail on the current user

    this function will return the detail on the user. we will spit out the
    `invalid_username` if user is not found.

    :return:
    """
    try:
        current_user_name = get_jwt_identity()
        user = get_user_by_name(current_user_name)
        if not user:
            data = {"msg": NO_USER_FOUND}
            return make_response(status_code=NO_CONTENT,
                                 data=data)
        user_obj = dict()
        user_obj['username'] = user.username
        user_obj['email'] = user.email
        user_obj['first_name'] = user.first_name
        user_obj['last_name'] = user.last_name
        user_obj['role'] = user.get_role()
        user_obj['force_password_change'] = user.force_password_change
        return make_response(data=user_obj)
    except OperationalError:
        abort(500, "db problem")
    except Exception as e:
        raise
        abort(500, "server problem")
