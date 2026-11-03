@echo off
set "DIR=%~dp0"
if exist "%DIR%venv\Scripts\python.exe" (
    "%DIR%venv\Scripts\python.exe" "%DIR%interface.py"
) else (
    echo Venv nao encontrado. Execute primeiro:
    echo   python -m venv venv
    echo   venv\Scripts\pip install -r requirements.txt
    pause
)
