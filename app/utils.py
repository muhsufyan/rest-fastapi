from passlib.context import CryptContext

# untuk enkrip kita gunakan algo bcrypt
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
# enkrip/hash password
def hash(password: str):
    # password dr client dienkrip/hash
    return pwd_ctx.hash(password)

# verifikasi password yg  tlh di encode/hash. plain_password didpt dari password client saat login sedangkan hashed password didpt dr database
def verifikasi_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)

