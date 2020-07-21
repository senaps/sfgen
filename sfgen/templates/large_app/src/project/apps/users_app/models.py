"""models for the users

this module contains all the abstractions for the classes and models that
we might need for the users app, allowing us for seperating the models from the
rest of the app. this module only contains the models and functionality related
to the models only. nothing related to the querying the db or handling the
views will be handled from here.

    - Role()  class representing the roles
    - User() class representing the users
"""
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='joined')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Role {self.name}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    force_password_change = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', remote_side=id, backref='created_by')

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return self.role.name
