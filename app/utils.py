from passlib.context import CryptContext

# untuk enkrip kita gunakan algo bcrypt
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
# enkrip/hash password
def hash(password: str):
    # password dr client dienkrip/hash
    return pwd_ctx.hash(password)