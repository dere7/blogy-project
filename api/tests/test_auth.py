"""test user view"""
import pytest
import json


@pytest.mark.parametrize(('email', 'password', 'first_name', 'last_name', 'profile_pic', 'error_message'), (
    ('testgmail.com', 'pass1234', 'first', 'last', None, b'Invalid email address.'),
    ('', 'pass1234', 'first', 'last', None, b'This field is required.'),
    ('test@gmail.com', '', 'first', 'last', None, b'This field is required.'),
    ('test@gmail.com', 'pass1234', '', 'last', None, b'This field is required.'),
    ('test@gmail.com', 'pass1234', 'first', '', None, b'This field is required.'),
    ('test@gmail.com', 'pass1234', 'first', 'last',
     'logo.png',  b'Invalid URL.'),
    ('johndoe@gmail.com', 'john1234', 'John', 'Doe',
     None, b'User with johndoe@gmail.com already exists.')
))
def test_register_validate_input(client, email, password, first_name, last_name, profile_pic, error_message):
    response = client.post('/user/', data={
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'profile_pic': profile_pic
    })
    assert response.status_code == 400
    assert error_message in response.data


def test_register(client):
    user = {
        'email': 'test@yahoo.com',
        'password': 'test123',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'profile_pic': 'https://lorem.picsum.com'
    }
    response = client.post('/user/', json=user)
    user.pop('password')
    assert response.status_code == 201
    assert response.is_json
    assert user == json.loads(response.json)


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
    assert response.status_code == 404
    assert b'Not found' in response.data


def test_login_incorrect_password(client):
    """tests login"""
    response = client.post('/user/login', data={
        'email': 'johndoe@gmail.com',
        'password': 'john12345'
    })
    assert response.status_code == 401
    assert b'Unauthorized' in response.data


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
