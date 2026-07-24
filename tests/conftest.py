import os
import pytest
from app import create_app
from app.database import init_db

@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app('testing')

    # Initialize a fresh test database
    with app.app_context():
        init_db(app.config['DATABASE_PATH'])

    yield app

    # Cleanup: remove test database after tests
    db_path = app.config['DATABASE_PATH']
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def client(app):
    """Provide a Flask test client for making requests."""
    return app.test_client()
