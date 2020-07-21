"""checkrs module

this module contains all the checkers we might need for the user's system

"""
import re

from ..query_handler import get_user_by_name
from project.config import EMAIL_PATTERN

def check_email(email):
    return re.match(EMAIL_PATTERN, email)


def check_user_exists(username):
    return True if get_user_by_name(username) else False
