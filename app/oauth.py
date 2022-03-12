from datetime import datetime, timedelta
from msilib import schema
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
import random
import string
from . import schema
from fastapi.security import OAuth2PasswordBearer
# skema untuk token bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET KEY, generate random dg panjang 32 karakter gabungan huruf kecil, huruf besar,( lewt ascii_letters), dan angka
SECRET_KEY = ''.join(random.choices(string.ascii_letters + string.digits, k = 32))
# algoritma yg digunakan
ALGORITMA = "HS256"
# waktu expire untuk tokennya, expire stlh 5 menit
WAKTU_EXPIRE_TOKEN_MENIT = 5

# buat token/generate token
def create_token(data: dict):
    data_will_encoded = data.copy()
    # expire adlh waktu sekarang ditambah 5 menit. agar waktunya sama kita gunakan utc
    expire = datetime.utcnow() + timedelta(minutes=WAKTU_EXPIRE_TOKEN_MENIT)
    # masukkan waktu expire ke dlm dict data yg akan di encode
    data_will_encoded.update({"exp":expire})
    # encode datanya jd token jwt
    tokenjwt= jwt.encode(data_will_encoded, SECRET_KEY, algorithm=ALGORITMA)
    return tokenjwt

# verifikasi token untuk otentifikasi
def verifikasi_token(token: str, credential_exception):
    try:
        print(token)
        # decode token
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
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credential", headers={"WWW-Authenticate":"Bearer"})
    return verifikasi_token(token, credential_exception)