

# AI Extraction Flask API

This project provides a Flask API to extract information such as name, phone number, skills, and education details (college name, university, graduation year) from text using the OpenRouter API with the meta-llama/llama-3.3-8b-instruct:free model.

## Features
- Extracts structured information from resume or profile text
- Uses OpenRouter's free Llama 3.3 8B Instruct model
- Modular codebase for easy extension

## File Structure
- `app.py`: Main Flask API entry point
- `openrouter_client.py`: Handles OpenRouter API communication
- `prompt_builder.py`: Builds the prompt for extraction
- `requirements.txt`: Python dependencies

## Setup Instructions

### 1. Clone the repository
```
git clone <your-repo-url>
cd AI-extraction
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure OpenRouter API Key
- Open `openrouter_client.py`
- Replace `YOUR_OPENROUTER_API_KEY` with your actual OpenRouter API key:
  ```python
  OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
  ```
- You can get a free API key from https://openrouter.ai/

### 4. Run the Flask API
```
python app.py
```

The API will be available at `http://127.0.0.1:5000/extract`

## Usage
Send a POST request to `/extract` with a JSON body containing the text to extract from:

```
curl -X POST http://127.0.0.1:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "John Doe\nPhone: 123-456-7890\nSkills: Python, Flask\nEducation: BSc Computer Science, MIT, 2022"}'
```

### Example Response
```
{
  "name": "John Doe",
  "phone": "123-456-7890",
  "skills": ["Python", "Flask"],
  "education": {
    "college": "MIT",
    "university": "MIT",
    "graduation_year": "2022"
  }
}
```

## Notes
- This API expects the text to be already extracted from PDF or image. For OCR or PDF text extraction, consider using Tesseract or PyMuPDF.
- The OpenRouter API may return slightly different JSON keys or formats depending on the input and model output.

## License
This project is open-source and free to use.