@echo off
setlocal EnableDelayedExpansion

:: Animation frames for loading
set "frames=- \ | /"

:: Function to show loading animation
:show_loading
set "message=%~1"
for /L %%i in (0,1,3) do (
    cls
    echo %message%
    echo !frames:~%%i,1!
    ping -n 1 127.0.0.1 > nul
)
goto :show_loading

:: Function to start loading in background
:start_loading
start /b cmd /c call loader.bat
set "loading_pid=%random%"
goto :eof

:: Function to stop loading
:stop_loading
taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq loader" >nul 2>&1
goto :eof

echo Starting AI Resume Information Extractor...
echo =======================================

REM Check if Python is installed
call :start_loading "Checking Python installation..."
where python >nul 2>&1
call :stop_loading
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.x from python.org
    echo Press any key to exit...
    pause >nul
    exit /b
)

REM Check if virtual environment exists, if not create one
if not exist "venv" (
    call :start_loading "Creating virtual environment..."
    python -m venv venv
    call :stop_loading
    
    call :start_loading "Installing required packages..."
    call venv\Scripts\activate
    pip install -r requirements.txt
    call :stop_loading
) else (
    call :start_loading "Activating virtual environment..."
    call venv\Scripts\activate
    call :stop_loading
)

REM Setup API keys
call :start_loading "Setting up API keys..."
python api_key_setup.py
call :stop_loading

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
endlocal
