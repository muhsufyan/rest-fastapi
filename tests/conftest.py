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