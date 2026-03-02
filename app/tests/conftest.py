import pytest
import os
from app import create_app, db

@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
        'JWT_SECRET_KEY': 'test-secret-key-that-is-long-enough-for-sha256',
        'ENCRYPTION_KEY': 'SSRq9YMvQWHlkqJL5gms-6PpDzaqO5RHssPc6yVEvY4=',
        'RATELIMIT_ENABLED': False,
        'RATELIMIT_STORAGE_URI': 'memory://',
    }

    app = create_app(config=test_config)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
