from bcrypt import hashpw, checkpw, gensalt
from flask_mongoengine import Document
from .. import db


class User(Document):
    """user model"""
    full_name = db.StringField(min_length=3, max_length=120, required=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(min_length=6, required=True)
    profile_pic = db.URLField()

    meta = {'indexes': ['email']}

    def check_password(self, password: str) -> bool:
        """checks if the password is correct"""
        return checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def to_dict(self):
        """returns dict"""
        return {
            'full_name': self.full_name,
            'email': self.email,
            'profile_pic': self.profile_pic
        }
