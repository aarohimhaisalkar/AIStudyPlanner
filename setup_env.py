#!/usr/bin/env python3
"""
Setup script to help configure the .env file
"""

import os

def setup_env_file():
    """Help user set up the .env file correctly"""
    
    print("🔧 AI Study Planner - Environment Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Read current content
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check if API key is still placeholder
        if 'your_openai_api_key_here' in content:
            print("❌ API key is still set to placeholder text")
            print("\n📝 Please follow these steps:")
            print("1. Go to: https://platform.openai.com/account/api-keys")
            print("2. Copy your API key (starts with 'sk-...')")
            print("3. Edit the .env file")
            print("4. Replace 'your_openai_api_key_here' with your actual API key")
            print("5. Save the file and restart the app")
            
            # Ask if user wants to update now
            user_input = input("\nDo you want to enter your API key now? (y/n): ")
            if user_input.lower() == 'y':
                api_key = input("Enter your OpenAI API key: ").strip()
                if api_key.startswith('sk-'):
                    # Update the file
                    new_content = content.replace('your_openai_api_key_here', api_key)
                    with open('.env', 'w') as f:
                        f.write(new_content)
                    print("✅ .env file updated successfully!")
                    print("🚀 You can now run: streamlit run app.py")
                else:
                    print("❌ Invalid API key format. API keys should start with 'sk-'")
        else:
            print("✅ API key appears to be configured")
    else:
        print("❌ .env file not found")
        print("Creating a new .env file...")
        
        with open('.env', 'w') as f:
            f.write("""# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
""")
        
        print("✅ .env file created")
        print("⚠️ Please edit the .env file and replace 'your_openai_api_key_here' with your actual API key")

if __name__ == "__main__":
    setup_env_file()
