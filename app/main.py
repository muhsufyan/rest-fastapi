import time
from click import option
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
"""
koneksi ke db dg psycopg2
RealDictCursor untuk mempermudah mapping & json
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
    alamat: str
    published: bool = True

# karena kita ingin terus terkoneksi maka hrs infinite loop sehingga jika error akan terlihat trs
while True:
# agar terkoneksi ke db
    try:
        con = psycopg2.connect(host="localhost",database="fastapi", user="root", password="password", port=5432, cursor_factory=RealDictCursor)
        # untuk sql statement
        cursor = con.cursor()
        # berhsl konek
        print("berhsl terhubung ke database")
        break
    except Exception as error:
        print("gagal terhubung ke database")
        print("Error : ", error)
        time.sleep(2)

@app.get("/showpost", tags=["create new data group"], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
async def show():
    # query
    cursor.execute(""" SELECT * FROM posts """)
    # fetch all data
    post = cursor.fetchall()
    return{
        "data": post
    }
@app.post("/createpost",status_code=status.HTTP_201_CREATED, tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
async def createdata2(tangkapdata: Post):
    
    # kode ini akan rentan terhdp sql injeksi yaitu
    # cursor.execute(f'INSERT INTO posts (nama, umur, alamat, published) VALUES ({tangkapdata.nama},{tangkapdata.umur},{tangkapdata.alamat},{tangkapdata.published})')
    # lbh tptnya pd bagian ({tangkapdata.nama},{tangkapdata.umur},{tangkapdata.alamat},{tangkapdata.published})

    # agar mencegah sql injeksi gunakan kode dibwh ini (urutan memengaruhi jd jgn salah menempatkan data)
    
    # query 
    cursor.execute(""" INSERT INTO posts (nama, umur, alamat, published) VALUES (%s, %s, %s, %s) RETURNING * """, (tangkapdata.nama, tangkapdata.umur, tangkapdata.alamat, tangkapdata.published))
    # hanya 1 data yg disimpan jd gunakan fecthone untuk fetch data (ini tdk menyimpan data tp hanya fetch, jika berhsl ditampilkan tp data tdk masuk ke db hanya ke memory sementara 
    # sehingga ketika di restart data akan hilang)
    data_baru = cursor.fetchone()
    # data simpan ke db
    con.commit()
    return {
        "data": data_baru
    }

@app.get("/showpost/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    data = cursor.fetchone()
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return{
        "data with id": data
    }

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["create new data group"], summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_post(id: int):
    # query
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    # fetch 1 data
    data = cursor.fetchone()
    # save to db
    con.commit()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/post/{id}", tags=["create new data group"], summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
async def update_post(id: int, data_update: Post):
    cursor.execute(""" UPDATE posts SET nama=%s, umur=%s, alamat=%s, published=%s WHERE id=%s RETURNING * """, (data_update.nama, data_update.umur, data_update.alamat, data_update.published, str(id)))
    # karena hanya 1 data yg di olah
    update_data = cursor.fetchone()
    # simpan ke db
    con.commit()
    if update_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    
    return {"data update": update_data}