from flask import Flask, request, jsonify
from openrouter_client import extract_info_with_llama
import fitz  # PyMuPDF
import io
import pytesseract
from PIL import Image, ImageEnhance
import tempfile
import re
from hf_enhance import HuggingFaceImageEnhancer

app = Flask(__name__)
hf_enhancer = HuggingFaceImageEnhancer()

def preprocess_for_phone(img):
    """Specific preprocessing for phone number extraction"""
    # Convert to grayscale
    img = img.convert('L')
    # Increase contrast to make text more visible
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # Increase size for better OCR
    if img.width < 1500:
        scale = 1500 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    return img

def is_valid_phone(number):
    """
    Check if a number is likely to be a valid phone number:
    - Should be 10-12 digits (excluding country code)
    - Should not be all same digits
    - Should not be sequential
    """
    # Clean the number first
    clean_num = re.sub(r'\D', '', number)
    
    # Check length (10-12 digits)
    if not (10 <= len(clean_num) <= 12):
        return False
        
    # Check if all digits are same (e.g., 9999999999)
    if len(set(clean_num)) == 1:
        return False
    
    return True

def extract_phone_numbers(text):
    # Multiple patterns for different phone number formats
    patterns = [
        # Numbers in parentheses (like in the CV header)
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

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    if not text.strip():
        ocr_text = []
        for page_num in range(len(doc)):
            pix = doc[page_num].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # Enhance with HuggingFace
            try:
                img = hf_enhancer.enhance_image(img)
                print(f"[DEBUG] Successfully enhanced PDF page {page_num + 1} with HuggingFace")
            except Exception as e:
                print(f"[WARNING] HuggingFace enhancement failed for PDF page {page_num + 1}: {str(e)}")
            ocr_text.append(pytesseract.image_to_string(img))
        text = "\n".join(ocr_text)
    return text

def extract_text_from_image(file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    
    # Try specific phone number extraction first
    phone_img = preprocess_for_phone(img)
    phone_text = pytesseract.image_to_string(phone_img)
    print("[DEBUG] Text from phone-optimized preprocessing:\n", phone_text)
    
    # Check for phone numbers in the phone-optimized text first
    phone_numbers = extract_phone_numbers(phone_text)
    
    # Regular enhancement and extraction for full text
    try:
        img = hf_enhancer.enhance_image(img)
        print("[DEBUG] Successfully enhanced image with HuggingFace")
    except Exception as e:
        print(f"[WARNING] HuggingFace enhancement failed: {str(e)}")
    
    # Extract full text
    text = pytesseract.image_to_string(img)
    print("[DEBUG] Text from regular OCR:\n", text)
    
    # If we found phone numbers in phone-optimized text, use that instead
    if phone_numbers:
        print("[DEBUG] Found phone numbers in optimized text:", phone_numbers)
        # Insert the phone number into the main text if it's not already there
        if not any(phone in text for phone in phone_numbers):
            text = f"Contact No.: {phone_numbers[0]}\n{text}"
    
    return text

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
            if filename.endswith('.pdf'):
                try:
                    extracted = extract_text_from_pdf(file_bytes)
                    print(f"[DEBUG] Extracted text from PDF {filename}:\n{extracted}")
                    texts.append(extracted)
                except Exception as e:
                    return jsonify({'error': f'Failed to extract text from PDF {filename}: {str(e)}'}), 500
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif')):
                try:
                    extracted = extract_text_from_image(file_bytes)
                    print(f"[DEBUG] Extracted text from image {filename}:\n{extracted}")
                    texts.append(extracted)
                except Exception as e:
                    return jsonify({'error': f'Failed to extract text from image {filename}: {str(e)}'}), 500
            else:
                return jsonify({'error': f'Unsupported file type: {filename}'}), 400
        text = "\n".join(texts)
        print(f"[DEBUG] Combined extracted text from all files:\n{text}")
    else:
        # Handle JSON text
        data = request.json
        text = data.get("text", "") if data else ""
        if not text:
            return jsonify({"error": "No text provided"}), 400
    # Extract phone numbers with regex
    phone_numbers = extract_phone_numbers(text)
    result = extract_info_with_llama(text)
    # If phone not found by LLM, add regex result
    if (isinstance(result, dict) and 'data' in result and (
        not result['data'].get('phone') or result['data'].get('phone') == ''
    )) and phone_numbers:
        result['data']['phone'] = phone_numbers
    elif (isinstance(result, dict) and 'phone' in result and (not result['phone'] or result['phone'] == '') and phone_numbers):
        result['phone'] = phone_numbers
    # Also always include regex result for reference
    result['regex_phone_numbers'] = phone_numbers
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
