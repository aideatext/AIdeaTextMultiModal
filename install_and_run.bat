@echo off
echo Setting up the AIdeaText environment...

:: Set the path to the AIdeaText installation directory
set AIdeaTextPath=%~dp0

:: Check for Python 3.11 installation
python --version 2>&1 | findstr "3.11" >nul
if %errorlevel% neq 0 (
    echo Python 3.11 is not installed. Downloading and installing Python 3.11.9...

    :: Set download URL and installation path
    set "pythonVersion=3.11.9"
    set "pythonDownloadUrl=https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe"
    set "installDir=%AIdeaTextPath%Python311"

    :: Check for curl installation
    where curl >nul 2>&1
    if %errorlevel% neq 0 (
        echo curl is not installed. Installing curl...
        :: Install curl silently
        start /wait "" "%AIdeaTextPath%curl\curl.exe" --silent --show-error --output "%TEMP%\curl-installer.exe" https://curl.se/windows/dl-7.79.1_2/curl-7.79.1_2-win64-mingw.zip
        :: Extract curl
        "%AIdeaTextPath%7zip\7z.exe" x -y -o"%AIdeaTextPath%curl" "%TEMP%\curl-installer.exe"
        :: Clean up installer
        del "%TEMP%\curl-installer.exe"
    )

    :: Download Python installer
    echo Downloading Python installer...
    curl --silent --show-error --output "%TEMP%\python-installer.exe" %pythonDownloadUrl%

    :: Install Python silently
    echo Installing Python...
    start /wait "" "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 DefaultCustomInstall=1 DefaultPath=%installDir%

    :: Clean up installer
    del "%TEMP%\python-installer.exe"

    :: Set the new Python path
    set "PATH=%installDir%;%installDir%\Scripts;%PATH%"
)

:: Verify the correct Python version is in use
python --version 2>&1 | findstr "3.11" >nul
if %errorlevel% neq 0 (
    echo Failed to verify Python 3.11 installation.
    exit /b 1
)

:: Navigate to the script directory
cd /d "%~dp0"

:: Create virtual environment using Python 3.11
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt

:: Download language models
echo Downloading language models...
call venv\Scripts\python.exe download_models.py

:: Run the application
echo Starting the AIdeaText application...
call venv\Scripts\python.exe app.py

:: Deactivate virtual environment
deactivate

pause
