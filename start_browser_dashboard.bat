@echo off
title CampusFix - Browser Dashboard Launcher
cd /d "%~dp0"

echo ========================================================================
echo     CAMPUS MAINTENANCE COMPLAINT ^& TRACKING SYSTEM - BROWSER DASHBOARD
echo ========================================================================
echo.
echo Starting local Python web server and connecting to SQLite...
echo Automatically opening dashboard in your default web browser...
echo.
echo If your browser does not open automatically, please open:
echo   http://localhost:8000
echo.
echo Press Ctrl+C in this console window to stop the server when done.
echo ========================================================================
echo.

python serve_web.py

pause
