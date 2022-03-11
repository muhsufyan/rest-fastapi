import time
from click import option
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy import false
# import model, konektor db sqlalchemy kita
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
"""
koneksi ke db dg sql alchemy
"""
# integrasi semua resource akses ke db, yaitu models dan konektor
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dokumentasi untuk api")


class Post(BaseModel):
    nama: str
    umur: int
    alamat: str
    published: bool = True

# endpoint untuk cek koneksi ke db
@app.get("/konektor", tags=["cek koneksi db"])
# gunakan dependency get_db untuk konek ke db yg bertipe session milik sqlalchemy
async def konekdb(db: Session = Depends(get_db)):
    # get semua data
    data = db.query(models.Post).all()
    # cek atribut database yg dpt diambil apa saja sekaligus cek query dlm bntk sqlnya
    print(db.query(models.Post)) # sama dg SELECT posts.id AS posts_id, posts.nama AS posts_nama, posts.umur AS posts_umur, posts.alamat AS posts_alamat, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts
    return {
        "message":"sukses terkoneksi ke db",
        "data":data
    }
@app.get("/showpost", tags=["create new data group"], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
async def show(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return{
        "data": data
    }
@app.post("/createpost",status_code=status.HTTP_201_CREATED, tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
async def createdata2(tangkapdata: Post, db: Session = Depends(get_db)):
    # menangkap dan simpan data dlm memory sementara
    data_baru = models.Post(nama=tangkapdata.nama, umur=tangkapdata.umur, alamat=tangkapdata.alamat, published=tangkapdata.published)
    """
    jika ingin lbh simpel gunakan kode sprt brkt
    print(**tangkapdata.dict())
    data_baru = models.Post(**tangkapdata.dict())
    """
    data = models.Post(**tangkapdata.dict())
    # simpan ke db
    db.add(data_baru)
    db.commit()
    db.refresh(data_baru)
    return {
        "data": data_baru,
        "dengan **":data
    }

@app.get("/showpost/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    # cetak query sqlnya
    print(db.query(models.Post).filter(models.Post.id == id))
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return{
        "data with id": data
    }

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["create new data group"], summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_post(id: int, db: Session = Depends(get_db)):
    # get data dg id
    data = db.query(models.Post).filter(models.Post.id == id)
    if data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    # simpan ke db
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}", tags=["create new data group"], summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
async def update_post(id: int, data_update: Post, db: Session = Depends(get_db)):
    cari_id = db.query(models.Post).filter(models.Post.id == id)
    data_cari = cari_id.first()
    if data_cari is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    cari_id.update(data_update.dict(), synchronize_session=False)
    # simpan ke db
    db.commit()
    
    return {"data update": data_update.dict()}