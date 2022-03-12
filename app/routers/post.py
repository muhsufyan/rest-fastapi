from .. import models, schema, oauth
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["data pribadi"]
)
@router.get("/showall", response_model= List[schema.PostResponse], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
# /showall?limit=n artinya 1 limit hanya menampilkan data sebanyak n 
async def show(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str]=""):
    print(limit)
    # kita ambil defaultnya 5 data untuk 1 limit, kemudian kita lewatkan/skip data sebanyak 0 data (defaultnya) misal
    # limit 5 dg skip 1 maka 1,3,5,7,9 limit ke 1, limit ke 2 yaitu 10,13,16,19 
    print(skip)
    # ini untuk pencarian misal /url?limit=x&skip=y&search=nama_yang_dicari atau /url?search=nama_yang_dicari
    data = db.query(models.Post).filter(models.Post.nama.contains(search)).limit(limit).offset(skip).all()
    return data
# tampilkan semua post yg dibuat oleh user yg login saja 
@router.get("/myposts", response_model= List[schema.PostResponse], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
async def show(db: Session = Depends(get_db), current_user: Session = Depends(oauth.get_current_user)):
    # dptkan semua data dr db dimana owner_id dr post adlh id user yg login saja
    data = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return data
    
@router.post("/createnew", response_model=schema.PostResponse, status_code=status.HTTP_201_CREATED, summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
# hrs login dulu melalui current_user: int = Depends(oauth.get_current_user)
async def createdata(tangkapdata: schema.CreatePostRequest,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth.get_current_user)):
    print(current_user)
    data_baru = models.Post(nama=tangkapdata.nama, umur=tangkapdata.umur, alamat=tangkapdata.alamat, published=tangkapdata.published, owner_id=current_user.id)
    db.add(data_baru)
    db.commit()
    db.refresh(data_baru)
    """
    jika ingin lbh simpel gunakan kode sprt brkt
    print(**tangkapdata.dict())
    data = models.Post(owner_id=current_user.id, **tangkapdata.dict())
    db.add(data)
    db.commit()
    db.refresh(data)
    """
    return data_baru

# hrs login dulu melalui current_user: int = Depends(oauth.get_current_user)
@router.get("/mypost/{id}", response_model=schema.PostResponse, summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth.get_current_user)):
    # tampilkan email dari user yg login
    print(current_user.email)
    data = db.query(models.Post).filter(models.Post.id == id).first()
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    # cek id yg login hrs sama dg owner_id dr post jika sama baru bisa melihat post
    # jika tdk sama maka beri notif bahwa dia tdk bisa meihat post
    if data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="aksi tidak diizinkan")
    return data

# hrs login dulu melalui current_user: int = Depends(oauth.get_current_user)
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_post(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth.get_current_user)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    data_query = db.query(models.Post).filter(models.Post.id == id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    # cek id yg login hrs sama dg owner_id dr post jika sama baru bisa delete
    # jika tdk sama maka beri notif bahwa dia tdk bisa delete
    if data.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="aksi tidak diizinkan")
    data_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# hrs login dulu melalui current_user: int = Depends(oauth.get_current_user)
@router.put("/update/{id}", response_model=schema.PostResponse, summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
async def update_post(id: int, data_update: schema.UpdatePostRequest,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth.get_current_user)):
    cari_id = db.query(models.Post).filter(models.Post.id == id)
    data_cari = cari_id.first()
    if data_cari is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    # cek id yg login hrs sama dg owner_id dr post jika sama baru bisa update
    # jika tdk sama maka beri notif bahwa dia tdk bisa update
    if data_cari.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="aksi tidak diizinkan")
    cari_id.update(data_update.dict(), synchronize_session=False)
    db.commit()
    return cari_id.first()