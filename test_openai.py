#!/usr/bin/env python3
"""
Test script to verify OpenAI API setup
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_openai_connection():
    """Test if OpenAI API is working correctly"""
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set up your .env file with your OpenAI API key")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Test API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello, OpenAI API is working!' in a friendly way."
                }
            ],
            max_tokens=50,
            temperature=0.5
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Test Successful!")
        print(f"Response: {result}")
        return True
        
    except openai.AuthenticationError as e:
        print(f"❌ Authentication Error: {e}")
        print("Please check your OpenAI API key")
        return False
        
    except openai.RateLimitError as e:
        print(f"❌ Rate Limit Error: {e}")
        print("You may have exceeded your API quota")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions"""
    print("\n" + "="*60)
    print("🔑 OpenAI API Setup Instructions")
    print("="*60)
    print("\n1. Get your API key from: https://platform.openai.com/account/api-keys")
    print("2. Copy your API key")
    print("3. Edit the .env file and replace 'your_openai_api_key_here' with your actual key")
    print("4. Save the .env file")
    print("5. Run this test script again")
    print("\n" + "="*60)

if __name__ == "__main__":
    print("🧪 Testing OpenAI API Setup...")
    print("-" * 40)
    
    success = test_openai_connection()
    
    if not success:
        show_setup_instructions()
    else:
        print("\n🎉 Your OpenAI API is ready to use!")
        print("You can now run: streamlit run app.py")
