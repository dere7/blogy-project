"""configures a test"""
import pytest
from mongoengine import disconnect
import bcrypt
from blogy import create_app
from blogy.models.user import User
from blogy.models.post import Post


@pytest.fixture
def app():
    '''configures flask app'''
    disconnect()
    app = create_app({
        'TESTING': True,
        'MONGODB_SETTINGS': [{
            'db': 'blogy_test',
            'connect': True
        }]
    })

    with app.app_context():
        user = User(full_name='John Doe', email='johndoe@gmail.com',
                    password=bcrypt.hashpw(b'john1234', bcrypt.gensalt())).save()
        post = {'title': 'test title',
                'body': 'test body',
                'cover_pic': None,
                'is_published': True,
                'tags': ['test', 'flask', 'mongdb']
                }
        Post(**post, author=user).save()

    yield app
    User.drop_collection()
    Post.drop_collection()
    disconnect()


@pytest.fixture
def client(app):
    '''creates a client to make requests to the application without
    running the server'''
    return app.test_client()


class AuthActions:
    '''handle auth'''

    def __init__(self, client):
        self._client = client

    def login(self, email='johndoe@gmail.com', password='john1234'):
        '''gets token'''
        response = self._client.post(
            '/user/login',
            data={'email': email, 'password': password}
        )
        return response.get_json().get('token')


@pytest.fixture
def auth(client):
    '''used for tests that requires auth'''
    return AuthActions(client)
