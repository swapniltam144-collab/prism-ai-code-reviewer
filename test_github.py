import asyncio
import os
from dotenv import load_dotenv

# Load environment BEFORE importing app modules
load_dotenv()

from app.github_service import fetch_pr_files

async def test_github():
    """Test if GitHub API is working"""
    
    # Check if GitHub token is loaded
    github_token = os.getenv("GITHUB_TOKEN")
    print(f"GitHub Token loaded: {github_token[:10]}..." if github_token else "❌ GitHub Token not found!")
    print(f"Token length: {len(github_token) if github_token else 0}\n")
    
    if not github_token or len(github_token) < 20:
        print("❌ ERROR: GITHUB_TOKEN is missing or invalid!")
        print("\nTo fix this:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token' → 'Generate new token (classic)'")
        print("3. Give it a name like 'AI Code Reviewer'")
        print("4. Select scopes: 'repo' (full control of private repositories)")
        print("5. Generate token and copy it")
        print("6. Update .env with: GITHUB_TOKEN=ghp_your_token_here")
        return
    
    # Using the repo from the URL you provided
    owner = "yugensys"
    repo = "agenticweb-api"
    pr_number = 1  # Change this to an actual PR number from the repo
    
    print(f"Testing GitHub API for {owner}/{repo} PR #{pr_number}...")
    
    try:
        files = await fetch_pr_files(owner, repo, pr_number)
        print(f"\n✅ Found {len(files)} changed files:")
        for f in files:
            print(f"  - {f['filename']} ({f.get('status', 'unknown')})")
            if f.get('patch'):
                print(f"    Changes: {len(f['patch'])} characters")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("- GitHub token is invalid or expired")
        print("- Token doesn't have 'repo' permissions")
        print("- PR number doesn't exist")
        print("- Repository is private and token doesn't have access")

if __name__ == "__main__":
    asyncio.run(test_github())
