import asyncio
import os
from dotenv import load_dotenv

# Load environment BEFORE importing app modules
load_dotenv()

from app.code_reviewer import analyze_code

async def test_deepseek():
    """Test if DeepSeek API is working"""
    
    # Check if API key is loaded
    api_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"API Key loaded: {api_key[:10]}..." if api_key else "❌ API Key not found!")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    
    if not api_key or len(api_key) < 20:
        print("\n❌ ERROR: DEEPSEEK_API_KEY is missing or invalid!")
        print("\nTo fix this:")
        print("1. Go to https://platform.deepseek.com/")
        print("2. Sign up or log in")
        print("3. Generate a new API key")
        print("4. Update environment.env with: DEEPSEEK_API_KEY=your_new_key")
        return
    
    sample_patch = """
@@ -1,3 +1,5 @@
 def calculate_total(items):
+    if not items:
+        return 0
     return sum(item.price for item in items)
"""
    
    print("\nTesting DeepSeek API...")
    try:
        result = await analyze_code("test.py", sample_patch)
        print("\n✅ DeepSeek Response:")
        print(result)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("- API key is invalid or expired")
        print("- No credits remaining on your DeepSeek account")
        print("- Network connectivity issue")

if __name__ == "__main__":
    asyncio.run(test_deepseek())
