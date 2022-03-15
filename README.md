## build aplikasi lengkap dg docker compose
pd dockerfile kita msh hrs mengetik perintah di terminal/cmd, sekarang kita simpan perintah docker tsb ke dlm file docker-compose.yaml<br>
untuk run perintah dlm docker-compose.yaml gunakan perintah <b>docker-compose up -d<b> -d artinya container berjln dibelakang layar/background<br>
untuk unbuild/hapus image gunakan perintah <b>docker-compose down<b><br>
ketika kita melakukan perubahan maka container aplikasi kita tdk berubah untuk mengeceknya perintah brkt <br>
<b>docker exec -it nama_container_aplikasi_kita bash</b><br>
<b>ls</b><br>
<b>cd app/</b><br>
<b>ls</b><br>
lihat file mainnya dg perintah <b>cat main.py</b><br>
untuk push image aplikasi kita dilwt karena kita tdk akan push ke docker hub<br>
untuk run compose dev dan prod gunakan perintah <br>
production<b>docker-compose -f docker-compose-dev.yaml up -d</b><br>
development<b>docker-compose -f docker-compose-prod.yaml up -d</b><br>
production<b>docker-compose -f docker-compose-dev.yaml down</b><br>
development<b>docker-compose -f docker-compose-prod.yaml down</b><br>