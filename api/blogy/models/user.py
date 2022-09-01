#!/usr/bin/env python3
"""Users model"""
from mongoengine import *
import bcrypt
from . import db


class User(db.Document):
    """User model that is used for auth"""
    first_name = db.StringField(max_length=120, min_length=2, required=True)
    last_name = db.StringField(max_length=120, min_length=2, required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.URLField()

    def check_password(self, password: str) -> bool:
        """Checks if the password is correct"""
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))
