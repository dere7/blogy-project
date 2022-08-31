"""users blueprint"""
from flask import Blueprint, jsonify, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
import bcrypt
from mongoengine import NotUniqueError
from .form import LoginForm, RegisterForm
from .models.user import User


bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/me')
@jwt_required()
def get_user():
    email = get_jwt_identity()
    user = User.objects(email=email).exclude('id', 'password').get_or_404()
    return jsonify(user)


@bp.route('/login', methods=['POST'])
def login():
    """
    POST /user/login
    * requires
        - email
        - password
    * returns
        - 400 with `{error: {email: [..], password: [..] }}` if not validated
        - 404 if user not found for the email
        - 401 if incorrect password
        - 200 with {token: '..'} if no error
    """
    form = LoginForm()
    if not form.validate():
        return jsonify({'error': form.errors}), 400

    user = User.objects(email=form.data['email']).get_or_404()
    if not user:
        abort(404)
    if not user.check_password(form.data['password']):
        abort(401)
    token = create_access_token(identity=user.email)
    return jsonify(token=token)


@bp.route('/', methods=['POST'])
def create_account():
    """
    POST / - create new user
    requires JSON body with fields
        - email
        - password
        - first_name
        - last_name
        - profile_pic(optional)
    returns
        - user
    """
    form = RegisterForm()
    if not form.validate():
        return jsonify(error=form.errors), 400
    try:
        user = User(
            email=form.data['email'],
            password=bcrypt.hashpw(
                form.data['password'].encode('utf8'), bcrypt.gensalt()),
            first_name=form.data['first_name'],
            last_name=form.data['last_name'],
            profile_pic=form.data['profile_pic'],
        ).save()
    except NotUniqueError:
        return jsonify(error=f'User with {form.data["email"]} already exists.'), 400

    user = User.objects(email=form.data['email']).exclude(
        'id', 'password').first()
    return jsonify(user.to_json()), 201
