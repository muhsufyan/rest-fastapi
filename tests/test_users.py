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

# konek ke db untuk testing
def overrid_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
# overwrite dependency get_db di semua routers controller jd overrid_get_db
from app.database import get_db
app.dependency_overrides[get_db] = overrid_get_db

# agar tdk perlu selalu memanggil client maka kita buat fixture decoratornya nantinya func dlm fixture akan dijdkan param
@pytest.fixture
def client():
    """blok kode ini akan run sblm TestClient"""
    # buat tabel database
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head")#jika memakai alembic
    """ dg yield maka ini sprti pembatas kode sblm yield akan dieksekusi dulu kemudian yield dan terakhir kode stlh yield baru dieksekusi
    jd alur run code-nya
    1. jlnkan kode sblm yield
    2. jlnkan kode yield
    3. jlnkan kode setlah yield
    pd kasus ini 
    1. jlnkan buat tabel db
    2. jlnkan TestClient untuk koneksi ke db dan melakukan operasi crud
    3. jlnkan hapus tabel db
    """
    yield TestClient(app)
    # blok kode ini akan run stlh TestClient dijalankan
    # hapus tabel database
    Base.metadata.drop_all(bind=engine)
    # command.downgrade("base")#jika memakai alembic

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
