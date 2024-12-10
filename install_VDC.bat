@echo off
REM Check if Python is installed
python --version
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python Version 3.7, or later.
    pause
    exit /B
)

REM Change to the directory where this BAT file is located
cd /d "%~dp0"

REM Create 'captions' folder if it does not exist
if not exist "captions\" (
    echo Creating 'captions' folder...
    mkdir captions
) else (
    echo 'captions' folder already exists.
)

REM Create a virtual environment
python -m venv venv
IF ERRORLEVEL 1 (
    echo Failed to create virtual environment. Please check your Python installation.
    pause
    exit /B
)

REM Activate the virtual environment
call .\venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required dependencies
pip install -r requirements.txt
IF ERRORLEVEL 1 (
    echo Failed to install required dependencies. Please check the requirements.txt file and your internet connection.
    pause
    exit /B
)

REM Separator and final message
echo =====================================================================
echo.
echo All files downloaded.
echo.
echo Setup completed successfully.
echo =====================================================================
echo.

pause