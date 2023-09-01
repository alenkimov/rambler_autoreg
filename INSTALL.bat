@echo off
poetry install
poetry run playwright install
@echo To start the script run "START.bat"
pause