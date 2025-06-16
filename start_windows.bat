@echo off
setlocal EnableDelayedExpansion

:: Function to show loading animation with message
:show_loading
set "message=%~1"
set "frames=-\|/"
for /L %%i in (0,1,3) do (
    cls
    echo %message%
    echo !frames:~%%i,1!
    ping -n 1 127.0.0.1 > nul 2>&1
)
goto :show_loading

echo Starting AI Resume Information Extractor...
echo =======================================

REM Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.x from python.org
    echo Press any key to exit...
    pause >nul
    exit /b
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
echo Setting up API keys...
python api_key_setup.py

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
