#!/bin/bash

echo "Starting AI Resume Information Extractor..."
echo "======================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed! Please install Python 3.x"
    echo "For Ubuntu/Debian: sudo apt-get install python3"
    echo "For Mac: brew install python3"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing required packages..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "Installing Tesseract OCR..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install tesseract
    else
        # Linux (Ubuntu/Debian)
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr
    fi
fi

# Install system dependencies for OpenCV
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Installing system dependencies..."
    sudo apt-get install -y libgl1-mesa-glx
fi

# Setup API keys
python3 api_key_setup.py

echo "Starting the server..."
echo "======================================="
echo "The application will be available at: http://localhost:5000"
echo
echo "Instructions:"
echo "1. Open your web browser"
echo "2. Go to http://localhost:5000"
echo "3. Upload your resume (PDF or Image)"
echo
echo "To stop the server, press Ctrl+C"
echo "======================================="

python3 app.py
