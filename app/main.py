from fastapi import Depends, FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

"""
enkrip password 
"""

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dokumentasi untuk api")

# panggil semua route post.py
app.include_router(post.router)
# panggil semua route user.py
app.include_router(user.router)
# panggil semua route atuh.py
app.include_router(auth.router)



    