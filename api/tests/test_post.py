'''tests posts'''


def test_create_post(auth):
    '''test POST / - create post'''
    token = auth.login()
    response = auth._client.post(
        '/', data={
            'title': 'test title',
            'body': 'test body',
            'cover_pic': None,
            'is_published': True,
            'tags': ['test', 'flask', 'mongdb']
        }, headers={
            'Authorization': f'Bearer {token}'
        }
    )
    assert response.status_code == 201
    assert b'test title' in response.data


def test_get_posts_paginated(client):
    '''tests GET /'''
    response = client.get('/')
    assert response.status_code == 200
    assert b'posts' in response.data


def test_get_post(client):
    '''tests GET /<slug>'''
    response = client.get('/test-title')
    assert response.status_code == 200
    assert b'test title' in response.data


def test_get_user_posts(auth):
    '''tests GET /me/posts'''
    token = auth.login()
    response = auth._client.get('/me/posts', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert b'test title' in response.data
    assert b'"email":"johndoe@gmail.com"' in response.data


def test_update_post(auth):
    '''tests POST /<slug>'''
    token = auth.login()
    response = auth._client.put(
        '/test-title',
        json={
            'body': 'another body'
        }, headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'test title' in response.data
    assert b'"body":"another body"' in response.data


def test_delete_post(auth):
    '''tests delete /<slug>'''
    token = auth.login()
    response = auth._client.delete(
        '/test-title',
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'Successfully deleted' in response.data
    response = auth._client.delete(
        '/test-title',
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 404


def test_publish(auth):
    '''test publish and unpublish endpoints'''
    token = auth.login()
    response = auth._client.put(
        '/test-title/unpublish',
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'"is_published":false' in response.data
    response = auth._client.put(
        '/test-title/publish',
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'"is_published":true' in response.data


def test_comment(auth):
    '''test comment endpoints'''
    token = auth.login()
    response = auth._client.post(
        '/test-title/comment',
        json={
            'content': 'nice post keep it up'
        },
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'nice post keep it up' in response.data

    # check inserted post
    response = auth._client.get(
        '/test-title/comment',
        headers={
            'Authorization': f'Bearer {token}'
        })
    assert response.status_code == 200
    assert b'nice post keep it up' in response.data
