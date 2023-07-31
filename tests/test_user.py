from app import schemas
from tests.database import client, session


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
