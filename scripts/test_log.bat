@echo off
cd /d "%~dp0.."
python -m src.main --log mylog.csv
pause