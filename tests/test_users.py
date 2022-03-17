from fastapi.testclient import TestClient
import pytest
from app.database import get_db
from app.main import app
from app import schema, models

# koneksi db untuk testing
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base
from alembic import command
from app.database import get_db
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

@pytest.fixture
def session():
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
@pytest.fixture
def client(session):
    # konek ke db untuk testing
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)


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
