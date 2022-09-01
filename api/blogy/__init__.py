#!/usr/bin/env python3
"""main flask server"""
from os import getenv
from flask_mongoengine import MongoEngine
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .models import db


def create_app(config=None):
    """main entry point for flask app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JWT_SECRET_KEY='super-secretttttt',  # Change this!
        WTF_CSRF_ENABLED=False,
        MONGODB_SETTINGS=[{
            "db": getenv('DB') or "project1",
            "host": getenv('DB_HOST') or "localhost",
            "port": getenv('DB_PORT') or 27017,
            "alias": "default",
        }]
    )

    JWTManager(app)
    if config:
        app.config.from_mapping(config)
    db.init_app(app)

    @app.route('/status')
    def status():
        """Checks status of server"""
        return jsonify({'status': 'OK'})

    @app.errorhandler(404)
    def not_found(m):
        """handle 404 error"""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(m):
        """handle 500 error"""
        return jsonify({'error': 'Internal Server Error'}), 500

    @app.errorhandler(401)
    def unauthorized(m):
        """handle 401 error"""
        return jsonify({'error': 'Unauthorized'}), 401

    from .user import bp
    app.register_blueprint(bp)

    return app
