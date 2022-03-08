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
	uvicorn main:app
run_autoreload:
	uvicorn main:app --reload