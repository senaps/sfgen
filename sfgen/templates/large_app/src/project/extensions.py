"""extensions and plugins initializer

this file will contain all the initializers and codes for extenstions and
plugins to be used in this application.
we will import the extenstion, initialize it nad then will configure it later
on in the `application` where they are going to be used.

   - db  SQLAlchemy instance to use the db in application
   - cors Cors instance to allow vuejs to send requests and get response
   - jwt JWTManager to handle user tokens and stuff

"""
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flasgger import Swagger


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

cors = CORS()
jwt=JWTManager()
swag = Swagger()
mg = Migrate()
