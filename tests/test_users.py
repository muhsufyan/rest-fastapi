import pytest
from app import schema
from jose import jwt
from app.config import settings

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

@pytest.mark.parametrize("email, password, expected_statuscode",[
    # kasus berhsl login
    ("email@email.com","password",200),
    # salah email
    ("email2@email.com","password",403),
    # salah password
    ("email@email.com","password12",403),
    # email kosong
    (None,"password",422),
    # password kosong
    ("email@email.com",None,422),
    # email dan password tdk ada
    ("email123@email.com","24password",403)
])

# def test_incorrect_login(test_user, client):
#     res = client.post(
#         '/login', data={'username': test_user['email'], 'password': 'salah'})

#     assert res.status_code == 403
#     assert res.json().get('detail') == 'invalid credential'

def test_incorrect_login(test_user, client, email, password, expected_statuscode):
    res = client.post(
        "/login", data={"username": email, "password": password})
    print(res.json().get("detail"))
    assert res.status_code == expected_statuscode
    # assert res.json().get("detail") == 'invalid credential'
