import json
import pytest

def register_and_login(client):
    """Helper function to register and login, returning a JWT token."""
    client.post('/auth/register',
        data=json.dumps({
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    response = client.post('/auth/login',
        data=json.dumps({
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    return response.get_json()['access_token']


def test_create_password_entry(client):
    token = register_and_login(client)
    response = client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert response.get_json()['id'] is not None


def test_create_password_missing_fields(client):
    token = register_and_login(client)
    response = client.post('/passwords/',
        data=json.dumps({'site_name': 'GitHub'}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 400


def test_get_all_passwords(client):
    token = register_and_login(client)
    # Create an entry first
    client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    response = client.get('/passwords/',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert 'entries' in response.get_json()
    assert 'pagination' in response.get_json()


def test_get_single_password(client):
    token = register_and_login(client)
    # Create an entry first
    create_response = client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    entry_id = create_response.get_json()['id']
    response = client.get(f'/passwords/{entry_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.get_json()['site_name'] == 'GitHub'


def test_update_password_entry(client):
    token = register_and_login(client)
    create_response = client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    entry_id = create_response.get_json()['id']
    response = client.put(f'/passwords/{entry_id}',
        data=json.dumps({'site_name': 'GitHub Updated'}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200


def test_delete_password_entry(client):
    token = register_and_login(client)
    create_response = client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token}'}
    )
    entry_id = create_response.get_json()['id']
    response = client.delete(f'/passwords/{entry_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200


def test_cannot_access_other_users_entry(client):
    # Create first user and entry
    token1 = register_and_login(client)
    create_response = client.post('/passwords/',
        data=json.dumps({
            'site_name': 'GitHub',
            'site_username': 'testuser',
            'password': 'mysecretpassword'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {token1}'}
    )
    entry_id = create_response.get_json()['id']

    # Create second user
    client.post('/auth/register',
        data=json.dumps({
            'username': 'testuser2',
            'email': 'test2@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    login2 = client.post('/auth/login',
        data=json.dumps({
            'email': 'test2@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    token2 = login2.get_json()['access_token']

    # Try to access first user's entry with second user's token
    response = client.get(f'/passwords/{entry_id}',
        headers={'Authorization': f'Bearer {token2}'}
    )
    assert response.status_code == 404