@echo off

call %~dp0venv\Scripts\activate

cd %~dp0

set TOKEN=5283101641:AAFHLqoynQNswFdIFFbHcE-Sct_uWhAYEIU

python yummy_bot.py

pause