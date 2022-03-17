from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
# from .config import setting

# ini dinon-aktifkan karena kita menggunakan alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dokumentasi untuk api")
# url yg diinzinkan
origins = [
    "https://www.google.com/",
    "http://localhost/"
]
# cors bawaan fastapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# panggil semua route post.py
app.include_router(post.router)
# panggil semua route user.py
app.include_router(user.router)
# panggil semua route atuh.py
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}




    