"""validates forms"""
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, URLField, StringField
from wtforms.validators import DataRequired, Email, Length, URL, Optional
from flask_mongoengine.wtf import model_form
from .models import user, post


class LoginForm(FlaskForm):
    """validate login form"""
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=6)])


# class RegisterForm(FlaskForm):
#     """validate signup form"""
#     first_name = StringField(
#         validators=[DataRequired(), Length(min=2, max=120)])
#     last_name = StringField(
#         validators=[DataRequired(), Length(min=2, max=120)])
#     email = EmailField(validators=[DataRequired(), Email()])
#     password = PasswordField(validators=[DataRequired(), ])
#     profile_pic = URLField(validators=[Optional(), URL(require_tld=False)])


RegisterForm = model_form(user.User)
