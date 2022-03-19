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
