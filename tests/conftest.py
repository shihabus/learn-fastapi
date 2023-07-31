from fastapi.testclient import TestClient
from app.main import app

import pytest

# to set up test DB
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# set up test DB
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # before the test yield
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # after the test yield


# create test_user
@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com", "password": "123"}
    res = client.post("/users", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    assert res.status_code == 201
    return new_user
