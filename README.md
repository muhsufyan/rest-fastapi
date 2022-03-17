## testing fitur users
refactor database test users
<ul>
    <li>buat testing untuk db testing</li>
    <li>buat testing untuk users <b>pytest -v -s tests\test_users.py</b></li>
    <li>ketika login agar fixture dpt berjln dlm scope module (dlm dir test) maka tambahkan scope="module", sblmnya tdk jln<br> karena scope default fixture adlh scope="function" jd setiap selesai 1 test maka tabel db akan dihapus. perubahan di tests/database.py</li>
    <li>jika kita pindahkan(run dulu) test login diatas test buat user maka akan error, ini menandakan test login bergantung ke tes buat user dan hal ini tdk boleh terjd<br> tdk boleh 1 tes bergantung pd tes lainnya</li>
    <li>ketika scope fixture default / function maka setiap run test akan dijlnkan fixture 1 kali (1 kali run untuk 1 test func)</li>
    <li>sedangkan scope fixture nya module maka setiap 1 module (1 file) maka akan dijlnkan 1 kali,<br> 
    artinya jika ada 2 file misal tests/test_post.py (ini akan dijlnkan 1 kali) dan tests/test_users.py (ini akan dijlnkan 1 kali)<br>
    maka fixture akan dijlnkan sebanyak 2 kali karena ada 2 module yaitu  tests/test_post.py & tests/test_users.py<br>
    sedangkan jika fixture scopenya function misal di tests/test_users.py ada 3 fungsi maka fixture akan dijlnkan 3 kali<br> dan jika dlm 2 module terdpt total 5 fungsi maka fixture scope function akan dijlnkan 6 kali,<br> itulah kenapa dg scope module maka test akan saling bergantung karena saat pertama kali dijlnkan pd kasus ini<br>
    database kosong sehingga hrs buat dulu user baru login tdk bisa login dulu baru buat user</li>
    <li>scope fixture session membuat fixture dijlnkan dlm 1 kali run mencakup semua test file <br> contohnya pd 2 module td dg scope fixture nya session maka fixture akan dijlnkan 1 kali saja untuk semua module (file) dan fungsi</li>
    <li>cara agar test fungsi tdk saling bergantung (independen) gunakan fixture scope default/function</li>

</ul>
