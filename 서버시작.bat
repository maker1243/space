@echo off
chcp 65001 >nul
title SALVAGE STATION Server
cd /d "%~dp0"

echo.
echo   SALVAGE STATION - LAN Server Launcher
echo   ======================================
echo.

REM Try python launcher first, then python, then py
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 server.py %*
    goto end
)

where python >nul 2>nul
if %errorlevel%==0 (
    python server.py %*
    goto end
)

echo   [ERROR] Python 3 not found.
echo.
echo   Install Python 3 from https://python.org
echo   Then double-click this file again.
echo.
pause

:end
pause
