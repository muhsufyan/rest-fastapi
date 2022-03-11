"""
https://www.pythonsheets.com/notes/python-sqlalchemy.html
sumber didpt dari
https://fastapi.tiangolo.com/tutorial/sql-databases/
file ini berfungsi sebagai konektor ke db
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# SQLALCHEMY_DATABASE_URL = <mysql+pymysql atau postgresql>://<username of db>:<password of db>@<ip of db>/<hostname of db>/<db name>
SQLALCHEMY_DATABASE_URL = "postgresql://root:password@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
from sqlalchemy_utils import database_exists, create_database
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    # engine.connect()
    # database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # returns a class to create each of the database models or classes (the ORM models). Base ini akan di expose sehingga kode yg mengimport Base ini dpt terkoneksi ke db
    # karena fungsinya sbg konektor
    Base = declarative_base()

# buat dependency agar terhub dan melakukan operasi pd model db melalui session. ini akan diimport 
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()