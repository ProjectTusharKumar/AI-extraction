import os
from dotenv import load_dotenv

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('OPENROUTER_API_KEY=\n')
        print("Created new .env file")

def get_api_key():
    """Get API key from user with clear instructions"""
    print("\n=== OpenRouter API Key Setup ===")
    print("You need an OpenRouter API key to use this application.")
    print("\nTo get your API key:")
    print("1. Go to https://openrouter.ai/")
    print("2. Sign up or login")
    print("3. Copy your API key from the dashboard")
    print("\nNote: The key starts with 'sk-or-v1-'")
    
    while True:
        key = input("\nEnter your OpenRouter API key (or press Ctrl+C to exit): ").strip()
        if key.startswith('sk-or-v1-'):
            return key
        else:
            print("\nError: Invalid API key format. Key should start with 'sk-or-v1-'")
            print("Please try again or press Ctrl+C to exit")

def save_api_key(key):
    """Save API key to .env file"""
    with open('.env', 'w') as f:
        f.write(f'OPENROUTER_API_KEY={key}\n')
    print("\nAPI key saved successfully!")

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

def main():
    try:
        # Load existing environment variables
        load_dotenv()
        
        # Check if API key already exists and is valid
        existing_key = os.getenv('OPENROUTER_API_KEY')
        if existing_key and existing_key.startswith('sk-or-v1-'):
            print("API key already configured.")
            return
        
        # Create .env file if needed
        create_env_file()
        
        # Get and save API key
        api_key = get_api_key()
        save_api_key(api_key)
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled. Please run the setup again to use the application.")
        exit(1)
    except Exception as e:
        print(f"\nError during setup: {str(e)}")
        print("Please try again or contact support.")
        exit(1)

if __name__ == "__main__":
    main()
