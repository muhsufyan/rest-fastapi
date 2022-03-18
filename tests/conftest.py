# koneksi db untuk testing
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base
from alembic import command
from app import schema, models
from app.oauth import create_token
"""
buat database baru untuk testing yaitu fastapi_test
"""
# SQLALCHEMY_DATABASE_URL = "postgresql://root:password@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
from sqlalchemy_utils import database_exists, create_database
if not database_exists(engine.url):
    create_database(engine.url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="module")
@pytest.fixture()
def session():
    print("debug untuk melihat fixture scope")
    # hapus tabel database
    Base.metadata.drop_all(bind=engine)
    # buat tabel database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
# setiap kali client dipanggil maka akan menjlnkan juga session
""" 
kelebihan metode ini selain dpt menjlnkan client pd func test juga dpt menjlnkan session (operasi db) dg menjdkannya
sebagai parameter. misal
def test_root(client,session):
    session.query(models.Post).all() #tambah operasi db ini
    res = client.get("/")
    assert res.json().get("message") == 'Hello World'
    assert res.status_code == 200
"""
# @pytest.fixture(scope="module")
@pytest.fixture()
def client(session):
    # konek ke db untuk testing
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    data_input = {"email":"email@email.com", "password":"password"}
    res = client.post('/akun/create', json=data_input)
    print(res.json())#debug
    data_baru = res.json()
    data_baru["password"] = data_input["password"]
    assert res.status_code == 201
    return data_baru

# buat token jwt untuk test
@pytest.fixture
def token(test_user):
    return create_token({"user_id":test_user['id']})

# untuk login jd untuk post yg hrs login akan menggunakan ini. ini perlu login data(client) dan token (token) sbg paramnya
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"bearer {token}"
    }
    return client

# buat post baru perlu data user yg buat post (test_user) dan koneksi operasi ke db(session)
@pytest.fixture
def test_posts(test_user, session):
    # karena published sdh ada nilai default jd kita lewat saja
    data_post =[
        {
            "nama": "string",
            "umur": 10,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 22,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 30,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 40,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 50,
            "alamat": "string",
            "owner_id": test_user['id']
        }
    ]
    # iterasi data dg map
    def create_post_model(data_post):
        return models.Post(**data_post)
    # map(func, data_post)
    data_map = map(create_post_model, data_post)
    data = list(data_map)
    # simpan data post diatas ke db dg sqlalchemy
    # session.add_all([models.Post({"field":"data"})])
    session.add_all(data)
    session.commit()
    data = session.query(models.Post).all()
    # print("===halo==="*30)
    # print(data[0].nama)
    return data

@pytest.fixture()
def test_user2(client):
    data_input = {"email":"email2@email.com", "password":"password2"}
    res = client.post('/akun/create', json=data_input)
    print(res.json())#debug
    data_baru = res.json()
    data_baru["password"] = data_input["password"]
    assert res.status_code == 201
    return data_baru
    
# buat post baru perlu data user yg buat post (test_user) dan koneksi operasi ke db(session)
@pytest.fixture
def test_posts2(test_user, session, test_user2):
    # karena published sdh ada nilai default jd kita lewat saja
    data_post =[
        {
            "nama": "string",
            "umur": 10,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 22,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 30,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 40,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "string",
            "umur": 50,
            "alamat": "string",
            "owner_id": test_user['id']
        },
        {
            "nama": "aku user 2",
            "umur": 60,
            "alamat": "string",
            "owner_id": test_user2['id']
        }
    ]
    # iterasi data dg map
    def create_post_model(data_post):
        return models.Post(**data_post)
    # map(func, data_post)
    data_map = map(create_post_model, data_post)
    data = list(data_map)
    # simpan data post diatas ke db dg sqlalchemy
    # session.add_all([models.Post({"field":"data"})])
    session.add_all(data)
    session.commit()
    data = session.query(models.Post).all()
    # print("===halo==="*30)
    # print(data[0].nama)
    return data