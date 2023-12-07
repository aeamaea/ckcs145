import pytest 

from app import app as flask_app

# This file inits our Flask app and fixtures that we need
# huh?

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()