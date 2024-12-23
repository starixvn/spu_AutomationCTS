@echo off
setlocal enabledelayedexpansion

:: Get the directory of the .bat file
set SCRIPT_DIR=%~dp0

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b 1
)

:: Install Playwright
echo Installing Playwright...
pip install playwright > install_log.txt 2>&1

:: Check the errorlevel after installing Playwright
if errorlevel 1 (
    echo [ERROR] Error occurred during Playwright installation. See install_log.txt for details.
    type install_log.txt
    pause
    exit /b 1
)

:: Install Playwright browsers
echo Installing Playwright browsers...
playwright install >> install_log.txt 2>&1

:: Check the errorlevel after installing Playwright browsers
if errorlevel 1 (
    echo [ERROR] Error occurred during Playwright browser installation. See install_log.txt for details.
    type install_log.txt
    pause
    exit /b 1
)

echo Playwright and its browsers have been installed successfully!

:: Install requirements from requirements.txt
if exist "%SCRIPT_DIR%requirements.txt" (
    echo Installing libraries from requirements.txt...
    for /f "tokens=*" %%L in (%SCRIPT_DIR%requirements.txt) do (
        echo Installing %%L...
        pip install %%L >> install_log.txt 2>&1
        if errorlevel 1 (
            echo [ERROR] Failed to install %%L. See install_log.txt for details.
            type install_log.txt
            pause
            exit /b 1
        )
    )
    echo All libraries from requirements.txt have been installed successfully!
) else (
    echo [ERROR] requirements.txt not found in the script directory.
    pause
    exit /b 1
)

pause
