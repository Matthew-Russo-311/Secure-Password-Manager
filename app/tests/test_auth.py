import json
import pytest

def test_register_success(client):
    response = client.post('/auth/register', 
        data=json.dumps({
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_register_duplicate_email(client):
    # Register first time
    client.post('/auth/register',
        data=json.dumps({
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    # Try to register again with same email
    response = client.post('/auth/register',
        data=json.dumps({
            'username': 'testuser2',
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 409

def test_register_missing_fields(client):
    response = client.post('/auth/register',
        data=json.dumps({'username': 'testuser'}),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_login_success(client):
    # Register first
    client.post('/auth/register',
        data=json.dumps({
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    # Then login
    response = client.post('/auth/login',
        data=json.dumps({
            'email': 'test@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_wrong_password(client):
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
            'password': 'wrongpassword'
        }),
        content_type='application/json'
    )
    assert response.status_code == 401

def test_login_invalid_email(client):
    response = client.post('/auth/login',
        data=json.dumps({
            'email': 'nobody@test.com',
            'password': 'test123'
        }),
        content_type='application/json'
    )
    assert response.status_code == 401