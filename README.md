## Login dengan menggunakan JWT
kita akan membuat login menggunakan JWT<br>
<ul>
    <li>buat dulu route untuk auth yaitu routers/auth.py</li>
    <li>buat route /login</li>
    <li>di utils.py buat fungsi verifikasi password yg  tlh di encode/hash</li>
    <li>panggil fungsi verifikasi password</li>
    <li>panggil route login di main.py</li>
    <li>install python-jose[cryptography] untuk generate dan verifikasi token jwt</li>
    <li>buat fungsi yg akan generate (create_token()) dan verifikasi  token jwt, di oauth.py</li>
    <li>untuk membuat secret key kita generate random. berikut sumber cara membuatnya<br> https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python<br>https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/</li>
    <li>form login perlu pip install python-multipart</li>
    <li>membuat schema filter request dan response untuk token</li>
    <li>pd oauth.py fungsi get_current_user akan mendptkan user yg login</li>
    <li>fungsi get_current_user akan menjd otentifikasi pd post yaitu di file post.py melalui Depends (hrs melalui get_current_user dulu baru bisa berjalan)</li>
    <li>operasi CUD pd post hrs melalui otentifikasi berupa buat token jwt lalu copas token kedlm header Authorization dg value "Bearer {tokennya}"</li>
</ul>