#!/usr/bin/env python3
"""Users model"""
from mongoengine import *
import bcrypt
from .. import db


class User(db.Document):
    """User model that is used for auth"""
    first_name = StringField(max_length=120, required=True)
    last_name = StringField(max_length=120, required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_pic = URLField()

    def check_password(self, password: str) -> bool:
        """Checks if the password is correct"""
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))
