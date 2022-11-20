# encoding:utf-8
from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class Users(db.Model):
    __tablename__ = 'jq_user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # gid = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self._password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = raw_password

    def check_password(self, raw_password):
        return self.password == raw_password
