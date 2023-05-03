@echo off
python -V
poetry update
poetry run playwright install
@echo To start the script run "start.bat"
pause