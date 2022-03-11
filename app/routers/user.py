from .. import models, schema, utils
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/akun",
    tags=["akun"]
)

@router.post("/create", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED, summary=["buat akun baru"], description="membuat akun baru")
def create_user(user: schema.CreateUserRequest, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    data_user_baru = models.User(**user.dict())
    db.add(data_user_baru)
    db.commit()
    db.refresh(data_user_baru)
    
    return data_user_baru

@router.get("/{id}", response_model=schema.UserResponse, summary=["tampilkan data akun dari id yg ditentukan"], description="menampilkan data akun dari id yg ditentukan lewat parameter url")
async def showspesific(id: int, db: Session = Depends(get_db)):
    data = db.query(models.User).filter(models.Post.id == id).first()
    print(db.query(models.User).filter(models.Post.id == id))
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data akun dengan id {id} tidak ditemukan'
                            )
    return data