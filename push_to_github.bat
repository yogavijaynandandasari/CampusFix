@echo off
setlocal

echo ========================================================
echo       CampusFix - Updating Author to yogavijaynandandasari
echo ========================================================
echo Repository: https://github.com/yogavijaynandandasari/campus-Fix.git
echo.

set "GIT_CMD=C:\Users\vijay nandan\.gemini\antigravity\scratch\mingit\cmd\git.exe"

cd /d "C:\Users\vijay nandan\.gemini\antigravity\scratch\Campus_Maintenance_System"

echo Pushing updated commit with your GitHub username (yogavijaynandandasari)...
echo.
"%GIT_CMD%" push --force origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! The project is now 100%% under YOUR username!
    echo   Check it now: https://github.com/yogavijaynandandasari/campus-Fix
    echo ========================================================
) else (
    echo.
    echo [ERROR] Push failed. Please try again.
)

echo.
pause
