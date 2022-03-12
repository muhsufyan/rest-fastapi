## QUERY PARAM
misalnya banyak post kita bagi jd beberapa bagian menggunakan paginasi sehingga<br>
hslnya ada url/post?page=1, url/post?page=2. key disini adlh page<br>
kasus kita keynya limit dg default 5 data (routers/post.py bagian showall) dg kata lain default 1 limit hanya menampilkan 5 data<br>misalnya /showall?limit=2 artinya 1 limit hanya menampilkan 2 data<br>
lalu kita lewat kan beberapa data dg skip, misal limit 5 dg skip 1 maka 1,3,5,7,9 limit ke 1, limit ke 2 yaitu 10,12,14,16<br>
http://127.0.0.1:8000/posts/showall?limit=5&skip=1 <br>
pencarian misal /url?limit=x&skip=y&search=nama_yang_dicari atau /url?search=nama_yang_dicari