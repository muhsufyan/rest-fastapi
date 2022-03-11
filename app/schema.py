from datetime import datetime
from pydantic import BaseModel, EmailStr
# handle data sekaligus validasi data input dr client (filter request)
class PostBase(BaseModel):
    nama: str
    umur: int
    alamat: str
    published: bool = True
# karena filter request buat data baru itu (data yg ditangkap ketika membuat data baru)
class CreatePostRequest(PostBase):
    pass
# filter request update data (data yg ditangkap ketika mengubah data lama jd baru / update)
class UpdatePostRequest(PostBase):
    pass
# filter response(data response yg dikirim ke client)
class PostResponse(PostBase):
    id: int
    class Config:
        orm_mode = True
# filter request akun 
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

# filter response akun
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True
