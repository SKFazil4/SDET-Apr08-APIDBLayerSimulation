import pytest
from fastapi.testclient import TestClient
from app_db.main import app
from app_db.db.session import SessionLocal

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def context():
    yield {}

@pytest.fixture
def db_session():
    session = SessionLocal()

    yield session

    session.rollback()
    session.close()