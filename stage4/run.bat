@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
echo Команды: аргументы программы, test - тесты, exit - выход.
:loop
set "ARGS="
set /p "ARGS=> "
if not defined ARGS goto loop
if /i "%ARGS%"=="exit" exit /b
if /i "%ARGS%"=="test" (
    python -m unittest discover -s tests -v
    goto loop
)
python src\main.py %ARGS%
goto loop
