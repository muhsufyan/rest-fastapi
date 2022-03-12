"""
https://www.pythonsheets.com/notes/python-sqlalchemy.html
sumber didpt dari
https://fastapi.tiangolo.com/tutorial/sql-databases/
file ini berfungsi sebagai konektor ke db
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = <mysql+pymysql atau postgresql>://<username of db>:<password of db>@<ip of db>:<port>/<hostname of db>/<db name>
# SQLALCHEMY_DATABASE_URL = "postgresql://root:password@localhost:5432/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
from sqlalchemy_utils import database_exists, create_database
if not database_exists(engine.url):
    create_database(engine.url)
else:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

# buat dependency agar terhub dan melakukan operasi pd model db melalui session. ini akan diimport 
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()