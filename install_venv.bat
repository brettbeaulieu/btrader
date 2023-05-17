@echo off
echo Installing venv and requirements...
call py -m venv .venv
call .venv\Scripts\activate.bat
call py -m pip install -r requirements.txt
