## cicd
<ul>
    <li>cicd sederhana</li>
</ul>
INI file .github/workflows/build-deploy.yaml
VERSI 1 ERROR

name: Build and Deploy Code
# bisa push/pull/ keduanya [push, pull_request]
# on:
#   push:
#   # push ke main branch saja dg isi branches: ["main"]
#     branches:
#     # push to multiple branch
#       - "main"
#       # - "branch lainnya"
#   pull_request:
#     branches:
#     - "test_branch"
on: [push, pull_request]
# jlnkan pekerjaan pekerjaan(lakukan pekerjaan dibwh ini)
jobs:
  # pekerjaan pertama
  job1: 
  # aplikasi berjln di ubuntu bersi terbaru
    runs-on: ubuntu-latest
      # lakukan langkah dibwh ini
      steps:
        # langkah pertama diberi nama
        - name: pulling git repo
        # lakukan perintah brkt
          uses: actions/checkout@v2
        # # langkah selanjutnya diberi nama
        # - name: install pip
        #   run: pip install
        # langkah selanjutnya diberi nama
        - name: hallo ini adalah perintah untuk menampilkan dg echo
          run: echo "ini yang ditampilkan"

VERSI 1 TDK ERROR

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: hallo world
        run: echo "ini ditampilkan"


VERSI 2 : INSTALL DEPENDENCIES

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt

VERSI 3 : INSTALL PYTEST DAN TESTING

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: install pytest
        run: |
          pip install pytest
      - name: test with pytest
        run: pytest -v -s

HASLNYA ERROR, INI WAJAR KARENA KITA TDK SET DATABASE DAN ENVIRONMENT VARIABELNYA
VERSI 4 : SET ENVIRONMENT VARIABEL SAMA SPRTI .ENV

name: Build and Deploy Code
on: [push, pull_request]
# # environment variabel bisa juga di set disini
# env:
#   db_hostname:localhost
#   db_port:5432
#   db_name:fastapi
#   db_username:root 
#   db_pass:password
#   jwt_secret_key:ini rahasia 
#   jwt_algoritma:HS256
#   jwt_expire:15
jobs:
  job1:
    # atur environment variabel
    env:
      db_hostname: localhost
      db_port: 5432
      db_name: fastapi
      db_username: root 
      db_pass: password
      jwt_secret_key: ini rahasia 
      jwt_algoritma: HS256
      jwt_expire: 15
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: install pytest
        run: |
          pip install pytest
          pytest


HASL VERSI 4 ERROR, INI WAJAR KARENA KITA SET ENVIRONMENT VARIABELNYA UNTUK LOKAL SEDANGKAN UNTUK GIT ACTION KITA HRS SET DULU
ENVIRONMENT VARIABELNYA DI Settings=>Secrets=>Actions=>New repository secret=>masukkan key dan value untuk environment variabel
VERSI 5 : SET ENVIRONMENT VARIABEL UNTUK DI GIT ACTION

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    # atur environment variabel
    env:
      db_hostname: ${{secrets.DB_HOSTNAME}}
      db_port: ${{secrets.DB_PORT}}
      db_name: ${{secrets.DB_NAME}}
      db_username: ${{secrets.DB_USERNAME}}
      db_pass: ${{secrets.DB_PASS}}
      jwt_secret_key: ${{secrets.JWT_SECRET_KEY}} 
      jwt_algoritma: ${{secrets.JWT_ALGORITMA}}
      jwt_expire: ${{secrets.JWT_EXPIRE}}
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: install pytest
        run: |
          pip install pytest
          pytest

HASIL VERSI 5 ERROR ITU WAJAR, TP SBLM FIX KITA AKAN BUAT DULU VERSI DARI ENVIRONMENT VARIABEL, KITA BUAT ENVIRONMENT VARIABEL UNTUK VERSI DEVELOP (NANTI DIBUAT UNTUK VERSI PRODUCTION). VERSI 5 EXTRA TDK RUN KARENA fitur New Environments hanya tersedia pada repo yg public sedangkan yg private tdk ada fiturnya. Untuk buat (jika public) Settings=>Environments=>New environments=>masukkan versi environment misalnya develop=>ok. stlh itu muncul Add Secret pilih Add Secret=>masukkan key dan value untuk environment variabel
VERSI 5 EXTRA : VERSI ENVIRONMENT VARIABEL UNTUK DEVELOP

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    # environment variabel versi develop
    environment:
      name: develop
    # atur environment variabel
    env:
      db_hostname: ${{secrets.DB_HOSTNAME}}
      db_port: ${{secrets.DB_PORT}}
      db_name: ${{secrets.DB_NAME}}
      db_username: ${{secrets.DB_USERNAME}}
      db_pass: ${{secrets.DB_PASS}}
      jwt_secret_key: ${{secrets.JWT_SECRET_KEY}} 
      jwt_algoritma: ${{secrets.JWT_ALGORITMA}}
      jwt_expire: ${{secrets.JWT_EXPIRE}}
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: install pytest
        run: |
          pip install pytest
          pytest


HSLNYA MSH ERROR KARENA KITA TDK INSTALL DATABASENYA
VERSI 6 : INSTALL DATABASE POSTGRESQL

name: Build and Deploy Code
on: [push, pull_request]
jobs:
  job1:
    # # environment variabel versi develop. untuk repo public
    # environment:
    #   name: develop
    # atur environment variabel
    env:
      db_hostname: ${{secrets.DB_HOSTNAME}}
      db_port: ${{secrets.DB_PORT}}
      db_name: ${{secrets.DB_NAME}}
      db_username: ${{secrets.DB_USERNAME}}
      db_pass: ${{secrets.DB_PASS}}
      jwt_secret_key: ${{secrets.JWT_SECRET_KEY}} 
      jwt_algoritma: ${{secrets.JWT_ALGORITMA}}
      jwt_expire: ${{secrets.JWT_EXPIRE}}
    
    # install service postgresql dlm container docker hub
    # https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers
    services:
      postgres:
        images: postgres
        env:
          POSTGRES_PASSWORD: ${{secrets.DB_PASS}}
          POSTGRES_DB: ${{secrets.DB_NAME}}_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: install python version 3.9
        # lewat ubuntu biasa 
        # uses: sudo apt install python
        # install python https://github.com/marketplace/actions/setup-python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: install pytest
        run: |
          pip install pytest
          pytest
