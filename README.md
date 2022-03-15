## migrasi database dengan alembic
misal ada penambahan field di suatu tabel maka struktur db hrs diubah<br>
mengubah secara manual itu sulit dan mahal maka kita gunakan migrasi, konsep ini ada di laravel, dll<br>
misal kita tambah kolom no hp di tabel post maka kita akan buat migrasi versi 2<br> 
<ul>
    <li>install alembic</li>
    <li>buat alembic yg disimpan pada suatu directory, kasus ini kita simpan dlm directory migrasidbv1 (migrasi database versi ke 1). jd perintahnya <b>alembic init migrasidbv1</b></li>
    <li>di migrasidbv1/env.py import database.py, ubah target_metadata jd bernilai Base.metadata, config.set_main_option("sqlalchemy.url") ini akan mengakses nilai petunjuk dibawah ini</li>
    <li>di alembic.ini set sqlalchemy.url jd sama sprti app.database.py yaitu SQLALCHEMY_DATABASE_URL sehingga bernilai <b>postgresql+psycopg2://root:password@localhost:5432/fastapi</b></li>
    <li>ubah lagi from app.models import Base</li>
    <li>ubah juga config.set_main_option("sqlalchemy.url",f'postgresql+psycopg2://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}') </li>
    <li>untuk generate database (migrate) perintahnya <b>alembic revision -m "nama generate"</b>, misal <b>alembic revision -m "v1 create table posts"</b></li>
    <li>nanti akan ada file baru migrasidbv1/versions/ nah itu adalh hsl generate</li> 
        <ul>
            <li>di func upgrade isi kode brkt (untuk membuat tabel posts, tanpa alamat)</li>
            <li><b> op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('nama', sa.String(), nullable=False),
                            sa.Column('umur', sa.Integer, nullable=False),
                            sa.Column("published", sa.Boolean, server_default="True", nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))</b></li>
            <li> di func downgrade isi kode brkt (menghapus tabel posts)</li>
            <li><b>op.drop_table('posts')</b></li>
        </ul>
    <li>cek work migrasi yg sekarang kita gunakan dg perintah <b>alembic current</b>, takutnya jika kita upgrade file migrasi yg salah jd cek dulu</li>
    <li>migrasi buat tabel posts ke db gunakan perintah "alembic upgrade {COPAS NILAI VARIABEL revision PD FILE HSL GENERATE, KASUS INI  migrasidbv1/versions/}"</li>
    <li><b>alembic upgrade 444acb4ddc7b</b></li>
    <li>kita buat migrasi baru dimana didlmnya akan ditambahkan field baru yaitu alamat</li>
    <li><b>alembic revision -m "v2 tambah field alamat"</b></li>
    <li>kode upgrade pd file migrasi baru untuk menambah field baru (alamat) pd tabel posts </li>
    <li><b>op.add_column('posts',sa.Column("alamat", sa.String, nullable=False))</b></li>
    <li>kode downgrade pd file migrasi baru untuk menghapus field baru (alamat) pd tabel posts </li>
    <li><b>op.drop_column('posts','alamat')</b></li>
    <li><b>alembic upgrade 28801a7e4404</b></li>
    <li><b>alembic heads</b></li>
    <li>hapus field alamat dg perintah dibwh ini</li>
    <li><b>alembic downgrade 444acb4ddc7b</b></li>
    <li>hapus tabel posts dg perintah dibwh ini</li>
    <li><b>alembic downgrade -1</b></li>
    <li>buat tabel users</li>
    <li><b>alembic revision -m "v3 buat tabel users"</b></li>
    <li>tambahkan kode pd fungsi upgrade dan downgrade sprti link ini https://github.com/Sanjeev-Thiyagarajan/fastapi-course/blob/main/alembic/versions/8c82b1632f52_add_user_table.py</li>
    <li> melihat history <b>alembic history</b></li>
    <li>migrasi semua struktur db ke db <b>alembic upgrade head<b></li>
    <li>tmbh foreign key ke tabel posts<b>alembic revision -m "v4 add foreign-key to posts table"</b></li>
    <li>tambahkan kode pd fungsi upgrade dan downgrade sprti link ini https://github.com/Sanjeev-Thiyagarajan/fastapi-course/blob/main/alembic/versions/af786b740296_add_foreign_key_to_posts_table.py</li>
    <li>migrasi semua struktur db ke db <b>alembic upgrade head<b></li>
    <li>kita tahu bahwa semua tabel ada di models.py jd ketika run file ini akan membuat tabel dan fieldnya langsung ke db<br>
    maka kita dpt mengenerate pembuatan file migrasi dg models.py td jd untuk vote, migrasi upgrade dan downgrade-nya<br>
    akan didpt dr auto-generate file models sehngga kita tdk perlu ngoding<br> caranya dg perintah dibwh ini</li>
    <li><b>alembic revision --autogenerate -m "v5 auto generate untuk vote"</b></li>
    <li>migrasi ke db dg perintah <b>alembic upgrade head</b></li>
    <li>dg ini kita dpt menghapus(komen dulu) <b>models.Base.metadata.create_all(bind=engine)</b> di main.py<br> dg create_all(bind=engine) maka otomatis sqlalchemy akan membuat struktur db dari models.py tp sekarang tdk lg<br>
    karena pembuatan struktur db dilakukan oleh alembic</li>
</ul>
