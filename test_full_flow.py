import asyncio
import os
from dotenv import load_dotenv

# Load environment BEFORE importing app modules
load_dotenv()

from app.github_service import fetch_pr_files, post_review_summary
from app.code_reviewer import analyze_code

async def test_full_flow():
    """Test the complete flow: GitHub → DeepSeek → Review"""
    
    print("Testing Full AI Code Review Flow\n")
    print("=" * 60)
    
    # Configuration
    owner = "swapniltam144-collab"
    repo = "prism-ai-code-reviewer"
    pr_number = 1
    
    print(f"\n Fetching PR files from GitHub...")
    print(f"   Repository: {owner}/{repo}")
    print(f"   PR Number: #{pr_number}\n")
    
    try:
        files = await fetch_pr_files(owner, repo, pr_number)
        print(f"✅ Found {len(files)} changed files\n")
        
        # Analyze only the first code file (skip .env files)
        files_with_patches = [
            f for f in files 
            if f.get("patch") and not f["filename"].endswith((".env", ".env.local"))
        ]
        
        if not files_with_patches:
            print("❌ No code files with changes found")
            return
        
        # Test with first code file only
        test_file = files_with_patches[0]
        print(f"2️⃣ Analyzing file: {test_file['filename']}")
        print(f"   Status: {test_file.get('status', 'unknown')}")
        print(f"   Changes: {len(test_file['patch'])} characters\n")
        
        print("3️⃣ Sending to DeepSeek AI for review...")
        ai_feedback = await analyze_code(test_file["filename"], test_file["patch"])
        
        print(f"\n✅ AI Review Complete!")
        print(f"   Found {len(ai_feedback)} review comments\n")
        
        print("4️⃣ Posting AI review summary comment to GitHub PR...")
        review_comments = []
        for c in ai_feedback:
            review_comments.append({
                "file": test_file["filename"],
                "line": c.get("line", 0),
                "severity": c.get("severity", "info"),
                "comment": c.get("comment", "")
            })
        resp = await post_review_summary(owner, repo, pr_number, review_comments)
        print(f"✅ PR comment posted (id: {resp.get('id', 'unknown')})\n")
        
        print("=" * 60)
        print("📝 AI Review Comments:")
        print("=" * 60)
        
        for idx, comment in enumerate(ai_feedback, 1):
            print(f"\n{idx}. Line {comment.get('line', 'N/A')}")
            print(f"   Severity: {comment.get('severity', 'info')}")
            print(f"   Comment: {comment.get('comment', 'No comment')}")
        
        print("\n" + "=" * 60)
        print("✅ Full flow test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_full_flow())
