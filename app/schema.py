from datetime import datetime
from pydantic import BaseModel
# handle data sekaligus validasi data input dr client (filter request)
class PostBase(BaseModel):
    nama: str
    umur: int
    alamat: str
    published: bool = True
# karena filter request buat data baru itu (data yg ditangkap ketika membuat data baru) sama sprti PostBase maka kita gunakan PostBase sbg argumen
# sehingga kita tdk perlu membuat lagi
class CreatePostRequest(PostBase):
    pass
# filter request update data (data yg ditangkap ketika mengubah data lama jd baru / update)
class UpdatePostRequest(PostBase):
    pass
# filter response(data response yg dikirim ke client)
class PostResponse(PostBase):
    id: int
    # created_at: datetime
    # agar data response mengikuti yg kita inginkan maka data hrs dlm bntk dict sehingga hrs menggunakan class Config
    class Config:
        orm_mode = True
