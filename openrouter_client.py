import requests
import json
import re
from prompt_builder import build_prompt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL = "meta-llama/llama-3.3-8b-instruct:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def extract_json_from_text(text):
    # Try to extract JSON from markdown code block or plain text
    code_block = re.search(r"```(?:json)?\n([\s\S]+?)```", text)
    if code_block:
        json_str = code_block.group(1)
    else:
        # Try to find the first { ... } block
        json_match = re.search(r"{[\s\S]+}", text)
        json_str = json_match.group(0) if json_match else text
    try:
        return json.loads(json_str), None
    except Exception:
        return None, json_str

def extract_info_with_llama(text):
    prompt = build_prompt(text)
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512
    }
    response = requests.post(OPENROUTER_URL, headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    result, raw = extract_json_from_text(content)
    if result is not None:
        return {"data": result, "explanation": content}
    else:
        return {"error": "Could not parse model output as JSON", "raw_output": content}
