@echo off
REM Install Python using the official installer if not already installed
REM You can replace the URL below with the latest Python installer URL
REM Uncomment the lines below if you need to install Python automatically

REM echo Downloading Python installer...
REM curl -o python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

REM echo Installing Python...
REM start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Verify Python installation
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python manually and rerun this script.
    exit /b 1
)

REM Upgrade pip to the latest version
python -m pip install --upgrade pip

REM Install OpenCV and NumPy
python -m pip install opencv-python numpy

REM Execute the Python script
python your_script.py

pause
