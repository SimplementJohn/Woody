@echo off
cd /d "%~dp0"
title BOT - Anzhelle V1.3

:loop
set DISCORD_TOKEN=Enter Your Token Here
py -3.13 .\main.py
echo Bot has stopped. Restarting...
timeout /t 2 /nobreak >nul
goto loop
