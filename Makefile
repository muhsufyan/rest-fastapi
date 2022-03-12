env_linux:
	source env/bin/activate
env_windows:
	develop\Scripts\activate.bat
	vscode,command pallete, Python: Select Interpreter, Enter.., .\develop\Scripts\python.exe
make_env:
	python3 -m venv <nama_virtual-environment>
fastapi:
	pip install fastapi
uvicorn:
	pip install uvicorn
requirements:
	pip install -r requirements.txt
run:
	uvicorn app.main:app
run_autoreload:
	uvicorn app.main:app --reload
create_db_table:
	python utils/db.py
sqlalchemy:
	pip install sqlalchemy
sqlalchemy_dbexist:
	pip install sqlalchemy_utils
emailvalid:
	pip install email-validator
bcrypt:
	pip install passlib[bcrypt]
jwt:
	pip install python-jose[cryptography]
form_login:
	pip install python-multipart