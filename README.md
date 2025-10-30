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
🧾 AI Resume Information Extractor

Make your hiring pipeline faster: this project extracts structured candidate information (name, contact, education, skills, etc.) from resumes in PDF or image formats using OCR + LLMs.

Built as a small, production-friendly Flask API that combines Tesseract OCR for text extraction with an LLM (via OpenRouter) to clean, validate, and structure the data.

## ✨ Highlights

- Fast OCR-powered text extraction from PDFs and images
- LLM-based post-processing for robust entity extraction (names, phone, email, education, skills)
- Multiple file upload support and debug logging for easy troubleshooting
- Extensible and easy to run locally or in a container

## 🚀 Features

- Extract text from scanned and digital resumes (PDF / JPG / PNG)
- Structured JSON output: name, phone, email, education, skills, experience snippets
- Intelligent phone/email extraction (regex + LLM validation)
- Batch/multiple uploads
- Clear logging and simple API for integration with ATS or dashboards

## 🧭 Typical Workflow

1. Client uploads resume PDF or image to the API endpoint.
2. Server runs Tesseract OCR to convert the document to raw text.
3. Raw text is passed to an LLM (OpenRouter client) with a prompt that extracts structured fields.
4. Post-processing cleans phone numbers, dates, and normalizes education/skills.
5. API returns structured JSON suitable for downstream systems (ATS, analytics).

## 🛠 Tech Stack

- Python + Flask — lightweight API
- Tesseract OCR — local OCR engine
- OpenRouter (or equivalent LLM provider) — LLM for parsing/validation
- Requests / HTTP client for API calls
- (Optional) Docker for containerized deployments

## ⚙️ Quick Start (Local)

Requirements:
- Python 3.8+ installed
- Tesseract OCR installed and available on PATH
- OpenRouter API key (or another LLM provider key)

1) Install Python deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Configure API key:

- Export `OPENROUTER_API_KEY` (or follow `api_key_setup.py` interactive flow)

```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

3) Run the app:

```bash
python app.py
```

4) Open the UI or use `curl` to POST files to `http://localhost:5000/upload` (or the route implemented in the code).

## 📬 Example API Response

```json
{
  "data": {
    "name": "Jane Doe",
    "phone": "+1-555-555-5555",
    "email": "jane.doe@example.com",
    "education": [
      {"institution": "University X", "degree": "B.Sc Computer Science", "year": "2020"}
    ],
    "skills": ["Python", "NLP", "Docker"]
  }
}
```

Adjust fields depending on the extraction prompt and downstream needs.

## 🧪 Testing & Development

- Use the provided start scripts (`start_windows.bat`, or the Unix start script if present) to create a venv and install deps.
- Add sample resumes in a `samples/` folder and run the upload endpoint to iterate quickly.

## 🐛 Troubleshooting

- OCR returns noisy text: try improving PDF/image quality or use deskewing/preprocessing.
- Tesseract not found: ensure Tesseract is installed and on your PATH (e.g., `tesseract --version`).
- LLM errors: confirm your `OPENROUTER_API_KEY` is valid and has quota.

## ♻️ Extending the Project

- Swap the LLM provider: update `openrouter_client.py` or add adapters for new providers.
- Add more structured fields: languages, certifications, project links.
- Add a small front-end or integrate a webhook to push results to an ATS.

## 🤝 Contributing

Contributions are welcome! Please open issues for bugs or feature requests and follow these steps:

1. Fork the repo
2. Create a branch `feat/my-feature`
3. Add tests / documentation
4. Open a pull request

## 📄 License

This project is open-source. Include your preferred license (e.g., MIT) or add a `LICENSE` file.

## 📬 Contact / Impressing a Recruiter

- Add a short project summary, your role, and the impact (e.g., "Reduced manual resume processing time by X%" or "Processed N resumes with Y accuracy") in this README or your portfolio page.
- Consider adding a short demo GIF or hosted example link in the repo description to make a strong impression.

---

If you'd like, I can also:

- Add a small `samples/` folder with example resumes and a test script that posts them to the API
- Create a minimal `Dockerfile` and `docker-compose.yml` for quick deployments

Let me know which of the above you'd like next and I'll implement it.

  2) Configure API key:

  - Export `OPENROUTER_API_KEY` (or follow `api_key_setup.py` interactive flow)

  ```bash
  export OPENROUTER_API_KEY="your_api_key_here"
  ```

  3) Run the app:

  ```bash
  python app.py
  ```

  4) Open the UI or use `curl` to POST files to `http://localhost:5000/upload` (or the route implemented in the code).

  ## 📬 Example API Response

  ```json
  {
    "data": {
      "name": "Jane Doe",
      "phone": "+1-555-555-5555",
      "email": "jane.doe@example.com",
      "education": [
        {"institution": "University X", "degree": "B.Sc Computer Science", "year": "2020"}
      ],
      "skills": ["Python", "NLP", "Docker"]
    }
  }
  ```

  Adjust fields depending on the extraction prompt and downstream needs.

  ## 🧪 Testing & Development

  - Use the provided start scripts (`start_windows.bat`, or the Unix start script if present) to create a venv and install deps.
  - Add sample resumes in a `samples/` folder and run the upload endpoint to iterate quickly.

  ## 🐛 Troubleshooting

  - OCR returns noisy text: try improving PDF/image quality or use deskewing/preprocessing.
  - Tesseract not found: ensure Tesseract is installed and on your PATH (e.g., `tesseract --version`).
  - LLM errors: confirm your `OPENROUTER_API_KEY` is valid and has quota.

  ## ♻️ Extending the Project

  - Swap the LLM provider: update `openrouter_client.py` or add adapters for new providers.
  - Add more structured fields: languages, certifications, project links.
  - Add a small front-end or integrate a webhook to push results to an ATS.

  ## 🤝 Contributing

  Contributions are welcome! Please open issues for bugs or feature requests and follow these steps:

  1. Fork the repo
  2. Create a branch `feat/my-feature`
  3. Add tests / documentation
  4. Open a pull request

  ## 📄 License

  This project is open-source. Include your preferred license (e.g., MIT) or add a `LICENSE` file.
