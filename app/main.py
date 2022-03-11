import time
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
# import schema yg tlh kita buat schema.py karena workdir nya sama dg main.py maka tinggal import dari . (maksudnya workdir nya sama)
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session
"""
schema, class Post(BaseModel) sebagai filter request dan response pindah ke schema.py
"""
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dokumentasi untuk api")

@app.get("/showpost", response_model= List[schema.PostResponse], tags=["create new data group"], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
async def show(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return data
    
@app.post("/createpost", response_model=schema.PostResponse, status_code=status.HTTP_201_CREATED, tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
# ubah tipe data param tangkapdata dari Post jd schema.Post karena class Post tlh dipindahkan ke schema.py
async def createdata(tangkapdata: schema.CreatePostRequest, db: Session = Depends(get_db)):
    data_baru = models.Post(nama=tangkapdata.nama, umur=tangkapdata.umur, alamat=tangkapdata.alamat, published=tangkapdata.published)
    db.add(data_baru)
    db.commit()
    db.refresh(data_baru)
    """
    jika ingin lbh simpel gunakan kode sprt brkt
    print(**tangkapdata.dict())
    data = models.Post(**tangkapdata.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    """
    return data_baru

@app.get("/showpost/{id}", response_model=schema.PostResponse, tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    print(db.query(models.Post).filter(models.Post.id == id))
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return data

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["create new data group"], summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_post(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id)
    if data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    data.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}", response_model=schema.PostResponse, tags=["create new data group"], summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
# ubah tipe data param data_update dari Post jd schema.Post karena class Post tlh dipindahkan ke schema.py
async def update_post(id: int, data_update: schema.UpdatePostRequest, db: Session = Depends(get_db)):
    cari_id = db.query(models.Post).filter(models.Post.id == id)
    data_cari = cari_id.first()
    if data_cari is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    cari_id.update(data_update.dict(), synchronize_session=False)
    db.commit()
    return cari_id.first()