@echo off
cd /d "%~dp0.."
python -m src.main --script scripts\start.txt
pause