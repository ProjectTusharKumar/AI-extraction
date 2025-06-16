import os
from dotenv import load_dotenv

def setup_api_keys():
    """Setup API keys if they're not already configured"""
    # Load existing environment variables
    load_dotenv()
    
    # Check for .env file
    if not os.path.exists('.env'):
        # Copy example file if it exists
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example, open('.env', 'w') as env:
                env.write(example.read())
    
    keys_updated = False
    
    # Check Hugging Face API key
    if not os.getenv('HUGGINGFACE_API_KEY'):
        print("\nHugging Face API Key Setup:")
        print("1. Go to https://huggingface.co/")
        print("2. Sign up or sign in")
        print("3. Go to Settings -> Access Tokens")
        print("4. Create a new token and copy it")
        key = input("\nEnter your Hugging Face API key: ").strip()
        update_env_file('HUGGINGFACE_API_KEY', key)
        keys_updated = True
    
    # Check OpenRouter API key
    if not os.getenv('OPENROUTER_API_KEY'):
        print("\nOpenRouter API Key Setup:")
        print("1. Go to https://openrouter.ai/")
        print("2. Sign up or sign in")
        print("3. Get your API key from the dashboard")
        key = input("\nEnter your OpenRouter API key: ").strip()
        update_env_file('OPENROUTER_API_KEY', key)
        keys_updated = True
    
    if keys_updated:
        print("\nAPI keys have been saved to .env file")
        # Reload environment variables
        load_dotenv()

def update_env_file(key, value):
    """Update a single key in the .env file"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f"{key}={value}\n")
        return

    # Read existing contents
    with open('.env', 'r') as f:
        lines = f.readlines()

    # Update or append the key
    key_updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            key_updated = True
            break
    
    if not key_updated:
        lines.append(f"{key}={value}\n")

    # Write back to file
    with open('.env', 'w') as f:
        f.writelines(lines)
