@echo off
echo Updating 'requirements.txt'...
call .venv\Scripts\activate.bat
call py -m pip freeze > requirements.txt
