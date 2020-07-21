"""decorators handling the user functionalities

this module contains the fucntions and decorators needed to override the way
user management should be working in the system.
we will try to not include any db queries in here and just load those types of
functionality from `query_handler` module instead.

"""
from functools import wraps

from flask_jwt_extended import (verify_jwt_in_request, get_jwt_claims,
                                get_jwt_identity)

from .query_handler import get_user_by_name
from .messages import ADMINS_ONLY
from project.apps.utils import make_response
from project.apps.utils.status_codes import NOT_ALLOWED

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_name = get_jwt_identity()
        current_user = get_user_by_name(current_user_name)
        current_user_role = current_user.get_role()
        if current_user_role != "Administrator":
            data= {"msg": ADMINS_ONLY}
            return make_response(data=data, status_code=NOT_ALLOWED)
        else:
            return fn(*args, **kwargs)
    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper