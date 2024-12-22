@echo off
setlocal enabledelayedexpansion

:: Colors for output
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

echo %GREEN%Finance Tracker Installation Script%NC%
echo ===============================
echo.

:: Function to print step
:print_step
echo %YELLOW%Step %~1: %~2%NC%
echo.
goto :eof

:: Check Python installation
call :print_step 1 "Checking Python installation"
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Python not found!%NC%
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo Python found successfully
echo.

:: Set up virtual environment
call :print_step 2 "Setting up virtual environment"
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to create virtual environment%NC%
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to activate virtual environment%NC%
    pause
    exit /b 1
)
echo Virtual environment created and activated
echo.

:: Upgrade pip
call :print_step 3 "Upgrading pip"
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to upgrade pip%NC%
    pause
    exit /b 1
)
echo Pip upgraded successfully
echo.

:: Install Finance Tracker
call :print_step 4 "Installing Finance Tracker"
python -m pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to install Finance Tracker%NC%
    pause
    exit /b 1
)
echo Finance Tracker installed successfully
echo.

:: Initialize application
call :print_step 5 "Initializing Finance Tracker"
python -m finance_tracker --init
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to initialize Finance Tracker%NC%
    pause
    exit /b 1
)
echo Finance Tracker initialized successfully
echo.

:: Run installation test
call :print_step 6 "Running installation test"
python test_installation.py
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Installation test failed%NC%
    pause
    exit /b 1
)
echo Installation test completed successfully
echo.

echo %GREEN%Installation completed successfully!%NC%
echo.
echo To start using Finance Tracker:
echo 1. Open a new Command Prompt
echo 2. Navigate to this directory:
echo    cd %CD%
echo 3. Activate the virtual environment:
echo    %YELLOW%venv\Scripts\activate%NC%
echo 4. Run Finance Tracker:
echo    %YELLOW%finance-tracker%NC%
echo.
echo For help, see:
echo - docs\QUICK_START.md
echo - docs\USER_MANUAL.md
echo - docs\TROUBLESHOOTING.md
echo.

pause
