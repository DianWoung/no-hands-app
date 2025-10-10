import pytest
from fastapi.testclient import TestClient

# We need to import the app to create a TestClient.
# This is now safe because we'll set a dummy API key before running pytest.
from app.main import app

@pytest.fixture(scope="module")
def client():
    """
    Provides a test client for the FastAPI application.
    """
    with TestClient(app) as c:
        yield c