# Testing Guide

## Quick Test Checklist

### ✅ Step 1: Environment Setup
```bash
# Check your environment.env has valid keys
cat environment.env
```

### ✅ Step 2: Start the Server
```bash
cd prism-ai-code-reviewer
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Visit: http://localhost:8000

### ✅ Step 3: Test DeepSeek API
```bash
python test_deepseek.py
```
Expected: JSON response with code review comments

### ✅ Step 4: Test GitHub API
```bash
# Edit test_github.py first - add your repo details
python test_github.py
```
Expected: List of files from a real PR

### ✅ Step 5: Test Webhook Locally
```bash
# In another terminal, with server running
python test_webhook.py
```
Expected: Response showing the webhook was processed

### ✅ Step 6: Test with Real GitHub (Optional)

**Option A: Using ngrok (Recommended for testing)**
1. Download ngrok: https://ngrok.com/download
2. Start your server: `uvicorn app.main:app --port 8000`
3. In another terminal: `ngrok http 8000`
4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. Go to GitHub repo → Settings → Webhooks → Add webhook
   - Payload URL: `https://abc123.ngrok.io/webhook/github`
   - Content type: `application/json`
   - Events: Pull requests
6. Create a test PR in your repo
7. Check ngrok terminal for incoming requests

**Option B: Deploy to a server**
- Deploy to Heroku, Railway, or any cloud platform
- Use the public URL for GitHub webhook

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Try: `uvicorn app.main:app --port 8001`

### DeepSeek API fails
- Verify `DEEPSEEK_API_KEY` in environment.env
- Check API quota at https://platform.deepseek.com/

### GitHub API fails
- Verify `GITHUB_TOKEN` has `repo` permissions
- Token format should be: `ghp_...`

### Webhook not triggering
- Check ngrok is running and URL is correct
- Verify webhook is set to "Pull requests" event
- Check GitHub webhook delivery logs

## Manual API Testing with curl

Test the webhook endpoint:
```bash
curl -X POST http://localhost:8000/webhook/github \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {"number": 1},
    "repository": {
      "name": "test-repo",
      "owner": {"login": "test-owner"}
    }
  }'
```
