## DATA PD OPERASI CRUD SBLM DISIMPAN KE DATABASE DG ORM SQLALCHEMY AKAN DILAKUKAN 
data akan disaring oleh file schema.py, fungsi file tsb sbg filter data antara user dengan database dg kata lain <br>
schema akan menjd filter untuk data request yg menuju ke db dan filter untuk data response yg menuju ke user untuk<br> ditampilkan disisi client
### lihat skema & arah tanda panah dibawah ini agar mengerti fungsi dr schema
#### client ==> schema ==> data : kita sbt dg filter request
#### cleint <== schema <== data : kita sbt dg filter response
