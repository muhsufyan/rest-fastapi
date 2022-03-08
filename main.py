from click import option
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
"""
data yg diberikan user hrs divalidasi. gunakan pydantic (BaseModel) & data ditangkap dulu kedlm class
INGAT jangan percaya apa yg diinput user (lakukan validasi agar aplikasi aman)
validasi jenis tipe data https://pydantic-docs.helpmanual.io/usage/types/
"""


app = FastAPI(title="Dokumentasi untuk api")

# class ini akan menangkap dan validasi tipe data yg diinput user
class Post(BaseModel):
    # nama hrs string dan umur hrs int
    nama: str
    umur: int
    # benarsalah: bool = True, kita beri nilai default yaitu True
    # cirifisik: Optional[str] = None, cirifisik adlh data yg bersifat optional (not required) tipe datanya hrs string. nilai defaultnya None

@app.post("/createpost2", tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
# data yg ditangkap berupa objek class Post yg tlh kita buat diatas, jd hanya nama dan umur saja yg diterima
async def createdata2(tangkapdata: Post):
    return {
        "nama": tangkapdata.nama,
        "umur": tangkapdata.umur,
        "data": tangkapdata.dict()
    }
"""
kita buat 4 skenario yaitu umur
1. nama dan umur ada 
    {"nama": "udin", "umur": 12} (status 200)
2. salah satunya tidak ada 
    {"umur": 12} (status 422)
3. data nama, umur, alamat 
    {"nama": "udin", "umur": 12, "alamat":"indonesia"} (status 200 tp alamat tdk ditangkap, good)
4. tipe data tdk sesuai 
    {"nama": "udin", "umur": "12"} (status 200, hrsnya 12 adlh int tp string msh masuk ??)
    {"nama": udin, "umur": 12} (status 422, nice)
    {"nama": 12, "umur": 12} (status 200)
    jd angka akan auto diconvert jd string
"""