@echo off
setlocal EnableDelayedExpansion

:: Ensure we're running from the batch file's location
cd /d "%~dp0"

echo Starting AI Resume Information Extractor...
echo =======================================

REM Check if Python is installed
set "PYTHON_EXE=C:\Users\itstu\AppData\Local\Microsoft\WindowsApps\python.exe"
if not exist "%PYTHON_EXE%" (
    echo Python is not installed! Please install Python 3.x from python.org
    echo Press any key to exit...
    pause >nul
    exit /b
)


REM Check and install Tesseract if not present
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo Tesseract is not installed. Installing now...
    
    if not exist "tools" mkdir tools
    cd tools
    
    echo Downloading Tesseract installer...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe' -OutFile 'tesseract-installer.exe'}"
    
    echo Installing Tesseract...
    tesseract-installer.exe /S /D=C:\Program Files\Tesseract-OCR
    
    echo Adding Tesseract to PATH for this session...
    set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"
    
    cd ..
    echo Tesseract installation completed!
    echo.
)

REM Check if virtual environment exists, if not create one
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing required packages...
    pip install -r requirements.txt
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

REM Setup API keys
echo.
echo Setting up API keys...
python api_key_setup.py
if %errorlevel% neq 0 (
    echo.
    echo Failed to set up API keys. Please try again.
    pause
    exit /b 1
)

cls
echo =======================================
echo Starting the server...
echo =======================================
echo The application will be available at: http://localhost:5000
echo.
echo Instructions:
echo 1. Open your web browser
echo 2. Go to http://localhost:5000
echo 3. Upload your resume (PDF or Image)
echo.
echo To stop the server, close this window or press Ctrl+C
echo =======================================

python app.py

pause
