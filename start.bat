@echo off
python -V
call .venv\Scripts\activate.bat
python -m rambler_autoreg
pause