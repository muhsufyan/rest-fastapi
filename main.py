from fastapi import FastAPI
# untuk memakai Body()
from fastapi.params import Body

# instance class FastAPI
app = FastAPI(title="Dokumentasi untuk api")

@app.get("/", tags=["index group"], summary=["tampilan pertama"], description="ini adalah keterangan untuk url index")
# func ini berjln scra asynchronous jika ingn synchronous hilangkan key async
async def root():
    return {"message":"hi ini pesan pertama"}

@app.post("/createpost", tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
# Body(...) akan menangkap data apapun dari user yg ditulis dlm bntk json misal {"nama": "udin", "umur": 12}
async def createdata(tangkapdata: dict=Body(...)):
    return tangkapdata

@app.post("/createpost2", tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
async def createdata2(tangkapdata: dict=Body(...)):
    return {
        "data baru": f'nama saya {tangkapdata["nama"]} dan umur saya {tangkapdata["umur"]}'
    }