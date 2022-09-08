from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, URLField
from wtforms.validators import Email, Length, DataRequired, URL, Optional
from flask_mongoengine.wtf import model_form
from blogy.models.user import User


RegisterForm = model_form(User)
LoginForm = model_form(User, only=['email', 'password'])


class UpdateUserForm(FlaskForm):
    """update user form"""
    full_name = StringField(
        validators=[Length(min=3, max=120)])
    email = EmailField(validators=[Email()])
    profile_pic = URLField(validators=[URL(), Optional()])
