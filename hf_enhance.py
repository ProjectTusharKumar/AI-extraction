from PIL import Image
import torch
from transformers import pipeline
import io
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HuggingFaceImageEnhancer:
    def __init__(self):
        # Initialize with CodeFormer model for reliable image enhancement
        self.api_url = "https://api-inference.huggingface.co/models/sczhou/codeformer"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
        }

    def enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Enhance image using CodeFormer model which is specifically designed for
        image restoration and enhancement
        Args:
            image: PIL Image to enhance
        Returns:
            Enhanced PIL Image
        """
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        # Convert to RGB if image is in RGBA mode
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Convert to base64
        encoded_image = base64.b64encode(img_byte_arr).decode('utf-8')

        try:
            # Call Hugging Face API with proper payload
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "inputs": encoded_image,
                }
            )
            response.raise_for_status()

            # Convert response back to PIL Image
            enhanced_image = Image.open(io.BytesIO(response.content))
            print("[DEBUG] HuggingFace enhancement successful")
            return enhanced_image

        except Exception as e:
            print(f"[WARNING] HuggingFace enhancement failed: {str(e)}")
            print("[INFO] Returning original image")
            return image  # Return original image if enhancement fails

# Alternative models you can try:
# - "stabilityai/stable-diffusion-x4-upscaler"
# - "CompVis/stable-diffusion-v1-4"
# - "nvidia/image-super-resolution"
