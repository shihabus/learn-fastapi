from fastapi.testclient import TestClient
from app import models
from app.main import app

import pytest

# to set up test DB
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.oauth2 import create_access_token

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


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@gmail.com", "password": "123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    # option: 1
    # session.add_all(
    #     [
    #         models.Post(
    #             title="Post 1", content="Content of post 1", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="Post 2", content="Content of post 2", owner_id=test_user["id"]
    #         ),
    #         models.Post(
    #             title="Post 3", content="Content of post 3", owner_id=test_user["id"]
    #         ),
    #     ]
    # )

    # option: 2
    sample_posts = [
        {
            "title": "Post 1",
            "content": "Content of post 1",
            "owner_id": test_user["id"],
        },
        {
            "title": "Post 2",
            "content": "Content of post 2",
            "owner_id": test_user["id"],
        },
        {
            "title": "Post 3",
            "content": "Content of post 3",
            "owner_id": test_user["id"],
        },
        {
            "title": "Post 4",
            "content": "Content of post 4",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_model = map(create_post_model, sample_posts)
    posts_model_list = list(posts_model)
    session.add_all(posts_model_list)

    session.commit()
    posts = session.query(models.Post).all()
    return posts
