import pytest
from jose import jwt

from app import schemas
from app.config import settings

# from tests.database import client, session


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "FASTAPI is running"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "hello@test.in", "password": "123"})
    schemas.UserOut(**res.json())
    assert res.json().get("email") == "hello@test.in"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    assert payload.get("user_id") == test_user["id"]
    # assert login_res["token_type"] == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("test@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
