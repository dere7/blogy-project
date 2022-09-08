"""test user view"""
import pytest
import json


@pytest.mark.parametrize(('email', 'password', 'full_name', 'profile_pic', 'error_message'), (
    ('testgmail.com', 'pass1234', 'first last', None, b'Invalid email address.'),
    ('', 'pass1234', 'first last', None, b'This field is required.'),
    ('test@gmail.com', 'pass1234', '', None, b'This field is required.'),
    ('test@gmail.com', '', 'first last', None, b'This field is required.'),
    ('test@gmail.com', 'pass1234', 'first last', 'logo.png',  b'Invalid URL.'),
    ('johndoe@gmail.com', 'john1234', 'John Doe', None,
     b'User with johndoe@gmail.com already exists.')
))
def test_register_validate_input(client, email, password, full_name, profile_pic, error_message):
    response = client.post('/user/', data={
        'email': email,
        'password': password,
        'full_name': full_name,
        'profile_pic': profile_pic
    })
    assert response.status_code == 400
    assert error_message in response.data


def test_register(client):
    user = {
        'email': 'test@yahoo.com',
        'password': 'test123',
        'full_name': 'Jane Doe',
        'profile_pic': 'https://lorem.picsum.com'
    }
    response = client.post('/user/', data=user)
    user.pop('password')
    assert response.status_code == 201
    assert response.is_json
    assert user == response.json


def test_login(client):
    """tests login"""
    response = client.post('/user/login', data={
        'email': 'johndoe@gmail.com',
        'password': 'john1234'
    })
    assert response.status_code == 200
    assert b'token' in response.data


def test_login_non_existent_account(client):
    """tests login"""
    response = client.post('/user/login', data={
        'email': 'johndoe12@gmail.com',
        'password': 'john1234'
    })
    assert response.status_code == 401
    assert b'Incorrect email or password' in response.data


def test_login_incorrect_password(client):
    """tests login"""
    response = client.post('/user/login', data={
        'email': 'johndoe@gmail.com',
        'password': 'john12345'
    })
    assert response.status_code == 401
    assert b'Incorrect email or password' in response.data


@pytest.mark.parametrize(('email', 'password', 'error_message'), (
    ('', 'pass1234', b'This field is required.'),
    ('test@gmma.com', '', b'This field is required.'),
    ('testgmma.com', 'pass1234', b'Invalid email address.'),
))
def test_login_validates_data(client, email, password, error_message):
    """validate email and password"""
    response = client.post('/user/login', data={
        'email': email,
        'password': password
    })
    assert response.status_code == 400
    assert error_message in response.data


def test_get_user(auth):
    """test /user/me endpoint"""
    token = auth.login()
    response = auth._client.get(
        '/user/me', headers={
            'Authorization': 'Bearer ' + token
        })
    assert response.status_code == 200
    assert b'email' in response.data


def test_get_user_without_token(auth):
    """test /user/me endpoint without token"""
    response = auth._client.get('/user/me')
    assert response.status_code == 401
    assert b'Missing Authorization Header' in response.data


def test_delete_user(auth):
    token = auth.login()
    response = auth._client.delete(
        '/user/me', headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert response.status_code == 200
    assert b'Successfully deleted' in response.data


def test_update_user(auth):
    token = auth.login()
    response = auth._client.put('/user/me', data={
        'full_name': 'Jane Doe',
        'email': 'janedoe@gmail.com',
        'profile_pic': 'https://lorem.picsum/'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert b'Jane Doe' in response.data


@pytest.mark.parametrize(
    ('full_name', 'email', 'profile_pic', 'error_msg'), (
        (None, 'janedoegmail.com', None, b'Invalid email address.'),
        (None, None, '/image.png', b'Invalid URL.'))
)
def test_update_user_validation(auth, full_name, email, profile_pic, error_msg):
    """tests validation of update user"""
    token = auth.login()
    user = {
        'full_name': full_name,
        'email': email,
        'profile_pic': profile_pic
    }
    response = auth._client.put('/user/me', data=user, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 400
    assert error_msg in response.data
