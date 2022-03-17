import pytest
from app import schema, models
from .database import client, session
from jose import jwt
from app.config import settings
@pytest.fixture()
def test_user(client):
    data_input = {"email":"email@email.com", "password":"password"}
    res = client.post('/akun/create', json=data_input)
    print(res.json())#debug
    data_baru = res.json()
    data_baru["password"] = data_input["password"]
    assert res.status_code == 201
    return data_baru

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == 'Hello World'
    assert res.status_code == 200
    # jika expected != data response maka hslnya ada - untuk expected dan + untuk data response

# unit test untuk create user
def test_create_user(client):
    res = client.post('/akun/create', json={"email":"email@email.com", "password":"password"})
    print(res.json())
    print(res.json())
    data = schema.UserResponse(**res.json())
    # test data response
    assert data.email == "email@email.com"
    # test status berhasil buat akun
    assert res.status_code == 201

def test_login(client, test_user):
    # res = client.post('/login', data={"username":"email@email.com", "password":"password"})
    res = client.post('/login', data={"username":test_user["email"], "password":test_user["password"]})
    print(res.json())#debug
    login_response = schema.Token(**res.json())
    payload = jwt.decode(login_response.token, settings.jwt_secret_key, algorithms=[settings.jwt_algoritma])
    # dptkan data yg ada dlm token. kasus ini datanya id
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.tipe_token == 'bearer'
    assert res.status_code == 200
