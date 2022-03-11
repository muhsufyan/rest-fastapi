# file ini untuk membuat model dari db, sekaligus untuk buat tabel
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
# import file database.py yg telah kita buat sblmnya, dimana fungsi database.py tsb sbg konektor ke db
from .database import Base
"""
setiap class merepresentasikan tabel
setiap column dlm class merepresentasikan atribut dari tabel(classnya)
"""
# tabel posts, Base as param sehingga terkoneksi ke db, ingat Base ada di database.py
class Post(Base):
    # nama tabel
    __tablename__="posts"
    # atribut/field pd tabel posts yaitu id, nama, umur, alamat, published
    id = Column(Integer, primary_key=True, nullable=False)
    nama = Column(String, nullable=False)
    umur = Column(Integer, nullable=False)
    alamat = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))