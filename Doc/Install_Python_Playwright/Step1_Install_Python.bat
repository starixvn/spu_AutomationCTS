@echo off
setlocal enabledelayedexpansion

:: Get the directory of the .bat file
set SCRIPT_DIR=%~dp0

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Starting installation...
    
    :: Set Python URL and installer path
    set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    set INSTALLER_PATH=%SCRIPT_DIR%python_installer.exe
    
    echo Downloading Python...
    powershell -Command "Invoke-WebRequest -Uri !PYTHON_URL! -OutFile !INSTALLER_PATH!"
    
    :: Check if the download was successful
    if errorlevel 1 (
        echo [ERROR] Failed to download Python installer. Please check your internet connection or URL.
        pause
        exit /b 1
    )

    echo Installing Python...
    start /wait "" "!INSTALLER_PATH!" /quiet InstallAllUsers=1 PrependPath=1 >install_log.txt 2>&1
    
    :: Check the errorlevel after installation
    if errorlevel 1 (
        echo [ERROR] Error occurred during Python installation. See install_log.txt for details.
        type install_log.txt
        pause
        exit /b 1
    )

    echo Python has been installed successfully!
    
    :: Delete the installer file
    del /f /q "!INSTALLER_PATH!"
    echo Installer file has been deleted!
    pause
) else (
    echo Python is already installed.
    pause
)
