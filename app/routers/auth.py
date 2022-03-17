
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# form untuk isi login
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app import schema
from .. import database, models, utils, oauth


router = APIRouter(
    tags=["/Authentication"]
)
@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # dg OAuth2PasswordRequestForm maka login akan menerima username & password untuk itu email jd username
    # ubah user_credentials.email jd user_credentials.username
    data_login = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if data_login is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credential")
    if not utils.verifikasi_password(user_credentials.password, data_login.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credential")
    # jika email dan passwordnya valid maka buat token, data yg akan masukkan kedlm token adlh id saja (nanti kalau ada role bisa dimasukkan)
    token = oauth.create_token(data={"user_id":data_login.id})
    return {
            "token":token,
            "tipe_token":"bearer"
            }
