import os
import pytest
import sys

sys.path.append(".")

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app
from app.routers.auth.models import ApiUser


load_dotenv()
USERNAME_TEST = os.getenv("API_USERNAME")
PASSWORD_TEST = os.getenv("API_PASSWORD")

TEST_SQLALCHEMY_DATABASE_URI = "postgresql://testuser:testpass@localhost:5435/test_db"
test_engine = create_engine(TEST_SQLALCHEMY_DATABASE_URI)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="module")
def test_session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    api_user = ApiUser(username=USERNAME_TEST,
                       password=PASSWORD_TEST, 
                       auth_level=1)
    session.add(api_user)
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def test_client(test_session):
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="module")
def test_user():
    return {"username": USERNAME_TEST, "password": PASSWORD_TEST}


@pytest.fixture(scope="module")
def test_token(test_client, test_user):
    response = test_client.post("/token", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token
