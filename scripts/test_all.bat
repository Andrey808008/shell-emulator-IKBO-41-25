@echo off
cd /d "%~dp0.."
python -m src.main --vfs test.zip --log mylog.csv --script scripts\start.txt
pause