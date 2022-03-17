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

# auto buat db & tabel database
Base.metadata.create_all(bind=engine)

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

# ini akan masuk ke db testing
client = TestClient(app)

def test_root():
    res = client.get("/")
    # print(res)# outputnya <Response [200]> perintahnya pytest -v -s tests\test_users.py
    # print(res.json())# outputnya {'message': 'Hello World'} perintahnya pytest -v -s tests\test_users.py
    # print(res.json().get("message"))# outputnya Hello World perintahnya pytest -v -s tests\test_users.py
    assert res.json().get("message") == 'Hello World'
    assert res.status_code == 200
    # jika expected != data response maka hslnya ada - untuk expected dan + untuk data response

# unit test untuk create user. jika kita run 2 kali maka akan error karena email sdh pernah disimpan (case in blm ada solusinya)
def test_create_user():
    res = client.post('/akun/create', json={"email":"email@email.com", "password":"password"})
    print(res.json())
    print(res.json())
    data = schema.UserResponse(**res.json())
    # test data response
    assert data.email == "email@email.com"
    # test status berhasil buat akun
    assert res.status_code == 201
