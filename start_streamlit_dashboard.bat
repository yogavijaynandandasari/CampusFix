@echo off
title CampusFix - Streamlit Dashboard Launcher
cd /d "%~dp0"

echo ========================================================================
echo   CAMPUS MAINTENANCE COMPLAINT ^& TRACKING SYSTEM - STREAMLIT DASHBOARD
echo ========================================================================
echo.
echo Launching Streamlit web dashboard in your browser...
echo.

python -m streamlit run app.py

pause
