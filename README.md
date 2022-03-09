## Refactor
sblmnya hanya ada file main.py saja, sekarang kita refactor. pindahkan main.py ke app
### buat folder baru, app berisi __init__.py (first run), main.py
ketika kita run dg uvicorn main:app maka akan menjlnkan main.py dan instance dr FastAPI.<br>
stlh kita pindahkan main.py ke app maka untuk run jd uvicorn app.main:app