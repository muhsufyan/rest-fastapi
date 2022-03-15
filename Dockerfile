# gunakan image python versi 3.9.7
FROM PYTHON:3.9.7

# PWD
WORKDIR /usr/src/app

# copas requirements.txt ke /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# copas semua folder & file projek ini ke workdir/pwd yaitu /usr/src/app
COPY . .

# run app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000","--reload"]