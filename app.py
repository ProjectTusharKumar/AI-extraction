from flask import Flask, request, jsonify, render_template_string
from openrouter_client import extract_info_with_llama
import fitz  # PyMuPDF
import io
import pytesseract
from PIL import Image, ImageEnhance
import tempfile
import re
from dotenv import load_dotenv

app = Flask(__name__)

# HTML template for the welcome page
WELCOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Information Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-section {
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            border: 2px dashed #3498db;
            border-radius: 5px;
        }
        .features {
            margin: 20px 0;
        }
        .features h2 {
            color: #2c3e50;
        }
        .features ul {
            list-style-type: none;
            padding: 0;
        }
        .features li {
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: monospace;
        }
        .api-example {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI Resume Information Extractor</h1>
        
        <div class="upload-section">
            <h2>Try it out!</h2>
            <form action="/extract" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp" multiple>
                <button type="submit">Extract Information</button>
            </form>
        </div>

        <div class="features">
            <h2>Features</h2>
            <ul>
                <li>📄 Extract text from PDF and image files</li>
                <li>👁️ OCR support for scanned documents</li>
                <li>📱 Smart phone number detection</li>
                <li>🎓 Education details extraction</li>
                <li>🛠️ Skills identification</li>
                <li>📁 Multiple file upload support</li>
            </ul>
        </div>

        <div class="features">
            <h2>API Usage</h2>
            <p>Send a POST request to <code>/extract</code> with either:</p>
            <ul>
                <li>Multipart form data with file(s)</li>
                <li>JSON with text content</li>
            </ul>
            
            <div class="api-example">
                <pre>
curl -X POST http://localhost:5000/extract \\
  -F "file=@resume.pdf"
                </pre>
            </div>
        </div>
    </div>
</body>
</html>
"""

def enhance_image(img):
    """Basic image enhancement for better OCR results"""
    # Convert to grayscale
    img = img.convert('L')
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # Resize if too small
    if img.width < 1500:
        scale = 1500 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    return img

def extract_phone_numbers(text):
    # Multiple patterns for different phone number formats
    patterns = [
        # Numbers in parentheses
        r'\((\d{10})\)',
        # Look for contact number specifically
        r'(?:Contact\s*No\.?\s*[:.]?\s*)(\d[\d\s\-]{7,}\d)',
        # Basic 10-digit number
        r'\b(\d{10})\b',
        # Number with country code
        r'(\+\d{1,3}[-\s]?\d{10})'
    ]
    
    found_numbers = set()
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            number = match.group(1)
            # Clean up the number
            clean_number = re.sub(r'\s+|-|\(|\)', '', number)
            if is_valid_phone(clean_number):
                found_numbers.add(clean_number)
    
    return list(found_numbers)

def is_valid_phone(number):
    """Check if a number is likely to be a valid phone number"""
    # Clean the number first
    clean_num = re.sub(r'\D', '', number)
    # Check length (10-12 digits)
    if not (10 <= len(clean_num) <= 12):
        return False
    # Check if all digits are same
    if len(set(clean_num)) == 1:
        return False
    return True

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    if not text.strip():
        ocr_text = []
        for page_num in range(len(doc)):
            pix = doc[page_num].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = enhance_image(img)
            ocr_text.append(pytesseract.image_to_string(img))
        text = "\n".join(ocr_text)
    return text

def extract_text_from_image(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    img = enhance_image(img)
    return pytesseract.image_to_string(img)

@app.route('/')
def welcome():
    """Welcome page with upload form and documentation"""
    return render_template_string(WELCOME_HTML)

@app.route('/extract', methods=['POST'])
def extract():
    texts = []
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        files = request.files.getlist('file')
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files provided'}), 400
        for file in files:
            filename = file.filename.lower()
            file_bytes = file.read()
            try:
                if filename.endswith('.pdf'):
                    texts.append(extract_text_from_pdf(file_bytes))
                elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif')):
                    texts.append(extract_text_from_image(file_bytes))
                else:
                    return jsonify({'error': f'Unsupported file type: {filename}'}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to process {filename}: {str(e)}'}), 500
        
        text = "\n".join(texts)
    else:
        data = request.json
        text = data.get("text", "") if data else ""
        if not text:
            return jsonify({"error": "No text provided"}), 400

    phone_numbers = extract_phone_numbers(text)
    result = extract_info_with_llama(text)
    
    if isinstance(result, dict) and 'data' in result:
        if not result['data'].get('phone') and phone_numbers:
            result['data']['phone'] = phone_numbers[0] if len(phone_numbers) == 1 else phone_numbers
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
