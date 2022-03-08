from click import option
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange #untuk generate id
"""
simpan data kedlm array
"""


app = FastAPI(title="Dokumentasi untuk api")

# berupa array dictionary
data_store = [{
    "id":1,
    "nama":"no name",
    "umur":43
    },
    {
    "id":2,
    "nama":"michael",
    "umur":23
},
]

class Post(BaseModel):
    nama: str
    umur: int
# fungsi ini akan mencari data dr id yg telah ditentukan, nantinya digunakan untuk menampilkan data yg dicari berdsr id
def find_data(id):
    for data in data_store:
        if data["id"] == id:
            return data

@app.get("/showpost", tags=["create new data group"], summary=["tampilkan data dari array"], description="menampilkan data array, hardcode")
async def show():
    return{
        "data": data_store
    }
@app.post("/createpost2", tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
async def createdata2(tangkapdata: Post):
    data_dict = tangkapdata.dict()
    # generate id
    data_dict['id'] = randrange(0, 1000000)
    # tambahkan data baru kedlm array dg bantuan append
    data_store.append(data_dict)
    return {
        "data": data_dict
    }

# NOTE JIKA KODE INI DISIMPAN DIAKHIR (STLH showspesific akan error), jd kita simpan sblm itu. USAHAKAN yg ada param url diletakkan terakhir
# menampilkan data yg terakhir dibuat
@app.get("/showpost/latest", tags=["create new data group"], summary=["tampilkan hanya data yg terakhir dibuat"], description="menampilkan data yg terakhir dibuat")
async def showslatestdata():
    data = data_store[len(data_store)-1]
    return{
        "data latest": data
    }

# show spesifik id
@app.get("/showpost/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
# id adalah int jd kalau string akan error
async def showspesific(id: int):
    data = find_data(id)
    return{
        "data with id": data
    }