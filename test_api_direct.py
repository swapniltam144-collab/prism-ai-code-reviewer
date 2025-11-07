import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def test_deepseek_direct():
    """Direct test of DeepSeek API"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    print(f"Testing DeepSeek API directly...")
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    print(f"API URL: https://api.deepseek.com/v1/chat/completions\n")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": "Say 'Hello, API is working!'"}
        ]
    }
    
    try:
        response = httpx.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}\n")
        
        if response.status_code == 401:
            print("❌ 401 Unauthorized - Your API key is invalid or expired")
            print("\nThis means:")
            print("1. The API key format is correct but the key itself is wrong")
            print("2. The key may have been revoked or expired")
            print("3. You need to generate a NEW key from DeepSeek platform")
            print("\nSteps to fix:")
            print("1. Go to: https://platform.deepseek.com/api_keys")
            print("2. Create a new API key")
            print("3. Copy the FULL key (starts with 'sk-')")
            print("4. Replace DEEPSEEK_API_KEY in .env file")
        elif response.status_code == 200:
            print("✅ Success! API key is valid")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_deepseek_direct()
