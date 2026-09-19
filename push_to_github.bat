@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo    CampusFix - Commit and Push to GitHub Repository
echo ========================================================
echo Target Repo: https://github.com/yogavijaynandandasari/CampusFix.git
echo.

cd /d "C:\Users\vijay nandan\.gemini\antigravity\scratch\Campus_Maintenance_System"

REM Check git command
set "GIT_CMD=git"
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    if exist "C:\Users\vijay nandan\.gemini\antigravity\scratch\mingit\cmd\git.exe" (
        set "GIT_CMD=C:\Users\vijay nandan\.gemini\antigravity\scratch\mingit\cmd\git.exe"
    ) else (
        echo [ERROR] Git was not found in PATH or mingit directory.
        pause
        exit /b 1
    )
)

echo [1/4] Staging all files...
"%GIT_CMD%" add .

echo [2/4] Committing updates...
"%GIT_CMD%" commit -m "feat: complete modern Streamlit web dashboard, Tkinter GUI, and analytics" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Everything is already committed or up to date.
)

echo [3/4] Ensuring remote origin is set...
"%GIT_CMD%" remote remove origin 2>nul
"%GIT_CMD%" remote add origin https://github.com/yogavijaynandandasari/CampusFix.git

echo [4/4] Pushing to main branch...
echo If prompted, sign in via browser or enter your GitHub Personal Access Token (PAT).
echo.
"%GIT_CMD%" push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   SUCCESS! All files pushed to GitHub:
    echo   https://github.com/yogavijaynandandasari/CampusFix
    echo ========================================================
    echo.
    echo Next Steps:
    echo 1. Open https://share.streamlit.io in your browser
    echo 2. Click "New app"
    echo 3. Select repository "yogavijaynandandasari/CampusFix"
    echo 4. Main file path: "app.py"
    echo 5. Click "Deploy!"
) else (
    echo.
    echo ========================================================
    echo [NOTE] If push was denied or asked for authentication:
    echo You can use a GitHub Personal Access Token (PAT):
    echo 1. Go to https://github.com/settings/tokens
    echo 2. Generate a classic token with "repo" scope
    echo 3. Run: git push https://TOKEN@github.com/yogavijaynandandasari/CampusFix.git main
    echo ========================================================
)

echo.
pause
