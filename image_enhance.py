import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from hf_enhance import HuggingFaceImageEnhancer

# Initialize HuggingFace enhancer
hf_enhancer = HuggingFaceImageEnhancer()

def enhance_image_for_ocr(img: Image.Image) -> Image.Image:
    """
    Enhanced pipeline that uses HuggingFace Real-ESRGAN first,
    then falls back to traditional CV methods if needed
    """
    # Try HuggingFace enhancement first
    try:
        img = hf_enhancer.enhance_image(img)
    except Exception as e:
        print(f"[WARNING] HuggingFace enhancement failed: {str(e)}")
        print("[INFO] Falling back to traditional enhancement")

    # Convert to grayscale for better OCR
    img = img.convert('L')
    # Resize image if it's too small to improve OCR accuracy
    if img.width < 1000:
        scale = 1000 / img.width
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
    # Convert PIL image to OpenCV format (numpy array)
    img_cv = np.array(img)
    # Apply adaptive thresholding to handle varying lighting conditions
    img_cv = cv2.adaptiveThreshold(img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10)
    # Convert back to PIL image for further processing
    img = Image.fromarray(img_cv)
    # Increase contrast to make text stand out
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    # Sharpen the image to make edges more distinct
    img = img.filter(ImageFilter.SHARPEN)
    # Denoise the image using a median filter
    img = img.filter(ImageFilter.MedianFilter(size=3))
    return img
