from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
# handle data sekaligus validasi data input dr client (filter request)
class PostBase(BaseModel):
    nama: str
    umur: int
    alamat: str
    published: bool = True

# filter response akun
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True
        
# karena filter request buat data baru itu (data yg ditangkap ketika membuat data baru)
class CreatePostRequest(PostBase):
    pass
# filter request update data (data yg ditangkap ketika mengubah data lama jd baru / update)
class UpdatePostRequest(PostBase):
    pass
# filter response(data response yg dikirim ke client)
class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True
# filter request akun 
class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str

# filter request untuk login
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

# filter response
class Token(BaseModel):
    token: str
    tipe_token: str

# filter response ketika sdh login
class TokenData(BaseModel):
    id: Optional[str] = None
# filter request untuk vote
class Vote(BaseModel):
    post_id: int
    # dir adalah vote, vote_dir= 0 artinya delete vote atau 1 artinya add vote. nilainya 1 atau 0 (hanya 1 nilai jd le=1)
    dir: conint(le=1)
class PostVoteResponse(BaseModel):
    post: PostResponse
    vote: int
    class Config:
        orm_mode = True
# IKUTI SPRTI DI UTUBE

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
