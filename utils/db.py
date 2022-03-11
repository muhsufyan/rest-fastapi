import psycopg2
from psycopg2.extras import RealDictCursor
def create_tables():
    # PERINTAH SQL BUAT DB DAN TABEL
	commands = (
			"""
			CREATE TABLE posts (
				id SERIAL PRIMARY KEY,
				nama VARCHAR(50) NOT NULL,
				umur INTEGER NOT NULL,
				alamat VARCHAR(100) NOT NULL,
				published BOOLEAN NOT NULL DEFAULT TRUE,
				create_at timestamptz NOT NULL DEFAULT NOW()
			)
	""")
	try:
		con = psycopg2.connect(host="localhost", database="fastapi", user="root", password="password", port=5432)
		# untuk sql statement
		cursor = con.cursor()
		# berhsl konek
		print("berhsl terhubung ke database")
		# BUAT DB
		# create table one by one
		cursor.execute(commands)
		# close communication with the PostgreSQL database server
		cursor.close()
		# commit the changes
		con.commit()

	except (Exception, psycopg2.DatabaseError) as error:
		print("gagal terhubung ke database")
		print("Error : ", error)
	finally:
		if con is not None:
			con.close()
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
if __name__ == '__main__':
	# try:
    con = psycopg2.connect(host="localhost", user="root", password="password", port=5432);
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # untuk sql statement
    cursor = con.cursor();
    # berhsl konek
    print("berhsl terhubung ke database");
	# Create table statement
    cursor.execute('create database fastapi;');
    # cursor.execute("DROP DATABASE fastapi;")
    cursor.close()
    create_tables()