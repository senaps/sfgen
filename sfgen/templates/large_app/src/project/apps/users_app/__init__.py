from flask import Blueprint

from ...extensions import db

auth = Blueprint("auth", __name__, url_prefix="/auth/")

from .views import *
BLUEPRINT = auth