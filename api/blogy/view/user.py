from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, jwt_required, create_access_token
from datetime import timedelta
from mongoengine import NotUniqueError
from bcrypt import hashpw, gensalt
from blogy.models.user import User
from blogy.forms.user_form import RegisterForm, LoginForm, UpdateUserForm
from .use_form import use_form

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/me')
@jwt_required()
def get_user():
    """
    GET /user/me
        - get current user info
    """
    return current_user.to_dict()


@bp.route('/', methods=['POST'])
@use_form(RegisterForm)
def create_account(form):
    """
    POST /user
        - create new account
    requires JSON body
        - email, full_name, password, profile_pic(optional)
    returns
        - created user or
        - 400 if error
    """
    try:
        user = User(**form.data)
        hashed_password = hashpw(form.password.data.encode(
            'utf8'), gensalt()).decode('utf8')
        user.password = hashed_password
        user.save()
    except NotUniqueError:
        return jsonify(error=f"User with {form.email.data} already exists."), 400
    return user.to_dict(), 201


@bp.route('/me', methods=['PUT'])
@jwt_required()
@use_form(UpdateUserForm)
def update_account(form):
    """
    PUT /user/me
        - update current user
    """
    form.populate_obj(current_user)
    current_user.save()
    return current_user.to_dict()


@bp.route('/me', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    DELETE /user/me
        - delete current user
    """
    current_user.delete()
    return jsonify(msg="Successfully deleted")


@bp.route('/login', methods=['POST'])
@use_form(LoginForm)
def login(form):
    """
    POST /user/login
        - gets token
    JSON Body
        - email, password
    """
    user = User.objects(email=form.email.data).first()
    if user and user.check_password(form.password.data):
        return jsonify(token=create_access_token(user, expires_delta=timedelta(days=30)))
    return jsonify(error='Incorrect email or password'), 401
