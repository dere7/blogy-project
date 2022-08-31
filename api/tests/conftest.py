"""configures a test"""
import pytest
from mongoengine import disconnect
import bcrypt
from blogy import create_app
from blogy.models.user import User


@pytest.fixture
def app():
    """configures flask app"""
    app = create_app({
        'TESTING': True,
        'DB': 'blogy_test'
    })

    with app.app_context():
        User(first_name='John', last_name='Doe',
             email='johndoe@gmail.com', password=bcrypt.hashpw(b'john1234', bcrypt.gensalt())).save()
    yield app
    User.drop_collection()


@pytest.fixture
def client(app):
    """creates a client to make requests to the application without
    running the server"""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email='johndoe@gmail.com', password='john1234'):
        response = self._client.post(
            '/user/login',
            data={'email': email, 'password': password}
        )
        return response.get_json().get('token')


@pytest.fixture
def auth(client):
    """used for tests that requires auth"""
    return AuthActions(client)
