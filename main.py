from click import option
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange 
"""
edit data dengan id tertentu. sama sprti post dimana kita perlu class yg akan menangkap dan validasi data yg di edit/update
jd untuk ini kita gunakan dulu saja class Post karena sama
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

def find_index(id):
    for i, data in enumerate(data_store):
        if data["id"] == id:
            return i

@app.get("/showpost", tags=["create new data group"], summary=["tampilkan data dari array"], description="menampilkan data array, hardcode")
async def show():
    return{
        "data": data_store
    }
@app.post("/createpost",status_code=status.HTTP_201_CREATED, tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
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


@app.get("/showpost/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int):
    data = find_data(id)
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return{
        "data with id": data
    }

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["create new data group"], summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    data_store.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}", tags=["create new data group"], summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
# tangkap data yg diupdate dg class Post, karena data yg diupdate itu = data ketika buat data baru (post)
async def update_post(id: int, data_update: Post):
    # cari index dari id data yg ingin diupdate
    index = find_index(id)
    # cek jika idnya tidak ada
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    # jika idnya ada, tangkap datanya dlm bntk dictionary
    data_dict = data_update.dict()
    # tangkap id dari data yg dicari
    data_dict["id"] = id
    # timpa data dari id dicari dg data baru dan letakkan di index yg sama sprti data sblmnya kedlm array tmpt disimpannya semua data (data_store)
    data_store[index] = data_dict
    return {"data update": data_dict}
