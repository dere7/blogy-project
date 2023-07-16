'''flask app'''
from os import getenv
from flask import Flask, jsonify
from mongoengine import connect
from flask_mongoengine import MongoEngine
from flask_jwt_extended import (JWTManager)
from flask_cors import CORS

db = MongoEngine()


def create_app(config=None):
    '''flask app factory'''
    app = Flask(__name__)
    app.config.from_mapping(
        JWT_SECRET_KEY=getenv('SECRET') or 'screttt',  # change this
        WTF_CSRF_ENABLED=False,
        MONGODB_SETTINGS=[{
            'db': getenv('DB') or 'blogy_dev',
            'host': getenv('DB_HOST') or 'localhost',
            'port': getenv('DB_PORT') or 27017,
            'alias': 'default',
        }]
    )
    CORS(app, resources={r"/*": {"origins": "*"}})
    jwt = JWTManager(app)
    if config:
        app.config.from_mapping(config)

    db.init_app(app)

    @jwt.user_lookup_error_loader
    def user_lookup_error_handler(_jwt_header, jwt_data):
        return jsonify(error=f'User with email `{jwt_data["sub"]}` not found'), 404

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.email

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        from .models.user import User
        return User.objects(email=identity).first()

    @app.route('/status')
    def status():
        """
        GET /status
            - gets status of a server
        """
        return jsonify(status='OK')

    @app.errorhandler(404)
    def bad_request(e):
        print(e)
        return jsonify(error=str(e)), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e)), 400

    from .view import user, post
    app.register_blueprint(user.bp)
    app.register_blueprint(post.bp)

    return app
