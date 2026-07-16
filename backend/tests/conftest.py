import pytest
from fastapi.testclient import TestClient

from app.main import app as fastapi_app
from app.database.session import engine
from app.database.base import Base
import app.models  # Import models to register them with Base.metadata


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Keep the SQLite database file for local reference, or we could drop tables if desired


@pytest.fixture
def client():
    return TestClient(fastapi_app)