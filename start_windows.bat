@echo off
setlocal

cd /d "%~dp0"

echo.
echo ================================
echo  AI Resume Information Extractor
echo ================================
echo.

:: --- CONFIGURE YOUR PATHS ---
:: Set your actual Python exe path here
set "PYTHON_EXE=C:\Users\itstu\AppData\Local\Programs\Python\Python313\python.exe"

:: Set your actual Tesseract exe path here
set "TESSERACT_EXE=C:\Program Files\Tesseract-OCR\tesseract.exe"

:: --- CHECK PYTHON ---
"%PYTHON_EXE%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found at: %PYTHON_EXE%
    pause
    exit /b 1
)

:: --- CHECK TESSERACT ---
"%TESSERACT_EXE%" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Tesseract not found at: %TESSERACT_EXE%
    pause
    exit /b 1
)

:: --- VENV SETUP ---
if not exist "venv" (
    echo Creating virtual environment...
    "%PYTHON_EXE%" -m venv venv
)

:: --- ACTIVATE VENV ---
call venv\Scripts\activate.bat
if not defined VIRTUAL_ENV (
    echo Error: Virtual environment activation failed.
    pause
    exit /b 1
)

:: --- UPGRADE PIP + INSTALL REQUIREMENTS ---
echo Installing dependencies...
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
)

:: --- API KEY SETUP ---
echo.
echo Setting up API keys...
python "%~dp0api_key_setup.py"
if %errorlevel% neq 0 (
    echo Failed to set up API keys. Please try again.
    pause
    exit /b 1
)

:: --- START THE APP ---
echo.
echo Starting AI Resume Information Extractor...
echo =======================================
echo The application will be available at: http://localhost:5000
echo.
echo Instructions:
echo 1. Open your web browser
echo 2. Go to http://localhost:5000
echo 3. Upload your resume (PDF or Image)
echo.

:: Optionally pass Tesseract location via env var (if your app uses it this way)
set TESSERACT_CMD=%TESSERACT_EXE%

python app.py

echo.
echo Press any key to exit...
pause >nul
