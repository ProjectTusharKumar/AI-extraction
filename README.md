# AI Resume Information Extractor

A Flask-based API that extracts structured information from resumes in PDF or image format. The application uses OCR (Optical Character Recognition) to extract text and OpenRouter's LLM API to process and structure the information.

## Features

- Extract text from PDF and image files
- OCR support for scanned documents
- Intelligent phone number extraction
- Structured information extraction (name, contact, education, skills)
- Support for multiple file uploads
- Debug logging for troubleshooting

## Requirements

- Python 3.x
- Tesseract OCR
- OpenRouter API Key

## Setup Instructions

### Windows Users

1. Install Python 3.x from [python.org](https://python.org)
2. Install Tesseract OCR:
   - Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to system PATH

3. Double-click `start_windows.bat`
   - Creates virtual environment
   - Installs required packages
   - Prompts for OpenRouter API key
   - Starts the server

### Linux/Mac Users

1. Make the start script executable:
```bash
chmod +x start_unix.sh
```

2. Run the start script:
```bash
./start_unix.sh
```

The script will:
- Install required system packages
- Create virtual environment
- Install Python packages
- Handle API key setup
- Start the server

## Usage

1. Start the application using the appropriate script
2. Open your web browser to `http://localhost:5000`
3. Upload your resume (PDF or image)
4. Get structured information including:
   - Name
   - Phone number
   - Education details
   - Skills
   - Other relevant information

## API Response Format

```json
{
  "data": {
    "name": "John Doe",
    "phone": "1234567890",
    "education": [
      {
        "college": "Sample University",
        "degree": "Bachelor's",
        "graduation_year": "2020"
      }
    ],
    "skills": ["Python", "JavaScript", "etc"]
  }
}
```

## Troubleshooting

- Check debug logs in the terminal for extraction details
- Ensure image/PDF is clear and readable
- Verify API key is correctly set up
- Make sure Tesseract OCR is properly installed

## Notes

- Works best with clear, well-formatted documents
- OCR accuracy depends on image quality
- Phone numbers are extracted using both regex and LLM
- Multiple phone number formats are supported

## License

This project is open-source and free to use.