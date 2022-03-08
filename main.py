from click import option
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 
"""
menyisipkan status kode. misal response ke user adlh data tdk ditemukan (404)
ini berkaitan dg response jd kita import dulu response
untuk set status nya kita gunakan status, import dulu
"""


app = FastAPI(title="Dokumentasi untuk api")

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
    data_dict['id'] = randrange(0, 1000000)
    data_store.append(data_dict)
    return {
        "data": data_dict
    }

@app.get("/showpost/latest", tags=["create new data group"], summary=["tampilkan hanya data yg terakhir dibuat"], description="menampilkan data yg terakhir dibuat")
async def showslatestdata():
    data = data_store[len(data_store)-1]
    return{
        "data latest": data
    }

@app.get("/showpost/codestatuscara1/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int, response: Response):
    data = find_data(id)
    # cek jika data dg id yg dicari tdk ada beri response dg status 404
    if not data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message":f'data dengan id = {id} tidak ditemukan'}
        # tp cara diatas "kurang bersih" sehingga kita bisa gunakan cara 2 sprti dibawah ini (kode diatas non aktif dulu) 
    return{
        "data with id": data
    }

@app.get("/showpost/codestatuscara2/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
# dg cara 2 ini param response: Response dpt dihapus, sehingga kode lbh clean
async def showspesific(id: int):
    data = find_data(id)
    # cek jika data dg id yg dicari tdk ada beri response dg status 404
    if not data: 
        # cara 2 dg httpexception (import dulu)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return{
        "data with id": data
    }