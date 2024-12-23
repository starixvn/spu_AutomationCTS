@echo off
setlocal enabledelayedexpansion

:: Get the directory of the .bat file
set SCRIPT_DIR=%~dp0

:: Check if VS Code is installed
code --version >nul 2>&1
if %errorlevel% neq 0 (
    echo VS Code is not installed. Starting installation...

    :: Set VS Code URL and installer path
    set VSCODE_URL=https://update.code.visualstudio.com/latest/win32-x64/stable
    set VSCODE_INSTALLER=%SCRIPT_DIR%VSCodeSetup.exe

    echo Downloading VS Code from %VSCODE_URL%
    powershell -Command "Invoke-WebRequest -Uri !VSCODE_URL! -OutFile !VSCODE_INSTALLER!"

    :: Check if the download was successful
    if exist "!VSCODE_INSTALLER!" (
        echo Downloaded VS Code installer successfully.
    ) else (
        echo [ERROR] Failed to download VS Code installer. Please check your internet connection or URL.
        pause
        exit /b 1
    )

    echo Installing VS Code...
    "!VSCODE_INSTALLER!" /silent > install_log.txt 2>&1

    :: Check the errorlevel after installation
    if errorlevel 1 (
        echo [ERROR] Error occurred during VS Code installation. See install_log.txt for details.
        type install_log.txt
        pause
        exit /b 1
    )

    echo VS Code has been installed successfully!

    :: Delete the installer file
    del /f /q "!VSCODE_INSTALLER!"
    echo Installer file has been deleted.
) else (
    echo VS Code is already installed.
)

pause
