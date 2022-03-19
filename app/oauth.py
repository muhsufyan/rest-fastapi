from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
import random
import string
from . import schema, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
# skema untuk token bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k = 32))
SECRET_KEY= settings.jwt_secret_key
ALGORITMA = settings.jwt_algoritma
WAKTU_EXPIRE_TOKEN_MENIT = settings.jwt_expire

# buat token/generate token
def create_token(data: dict):
    data_will_encoded = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=WAKTU_EXPIRE_TOKEN_MENIT)
    data_will_encoded.update({"exp":expire})
    tokenjwt= jwt.encode(data_will_encoded, SECRET_KEY, algorithm=ALGORITMA)
    return tokenjwt

# verifikasi token untuk otentifikasi
def verifikasi_token(token: str, credential_exception):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMA])
        # dptkan data yg ada dlm token. kasus ini datanya id
        id: str = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schema.TokenData(id = id)
    except JWTError as e:
        print(e)
        raise credential_exception
    except AssertionError as e:
        print(e)
    return token_data

# dptkan data siapa yg login
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credential", headers={"WWW-Authenticate":"Bearer"})
    # verifikasi token dan dptkan data dari token (claim/payloadnya)
    token = verifikasi_token(token, credential_exception)
    # cari data user dari token berupa id ke database, SELECT * FROM users WHERE id = id
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user