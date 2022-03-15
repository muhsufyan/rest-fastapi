## fitur dan tabel vote
saat melakukan vote/like maka 1 user hanya boleh 1 kali vote/like <br>
<ul>
    <li>buat class Vote baru di models yg berisi foreign key id users dan foreign key id posts</li>
    <li>buat route /vote di routers/vote.py</li>
    <li>id users didpt dr ekstrak token jwt (dr claim/payload jwt yg berupa id users)</li>
    <li>id posts didpt ketika users memvote suatu post tertentu</li>
    <li>vote = 1 artinya add vote, vote = 0 artinya delete vote. format jsonnya {post_id=id post yg dipilih, vote_dir= 0 artinya delete vote atau 1 artinya add vote}</li>
    <li>buat schema untuk vote</li>
    <li>format vote. {"post_id": id post yg ingin di add vote/delete vote dlm int, "dir":1 atau 0 berupa int}. urlnya /vote/ dg method post</li>
</ul>
