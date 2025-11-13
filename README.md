# AI Code Reviewer

Automated AI-powered code review bot for GitHub Pull Requests using DeepSeek AI.

## Deploy to HuggingFace Spaces

1. Create a new Space on HuggingFace (select Docker SDK)
2. Push this repo to your Space
3. Add secrets in Space settings:
   - `GITHUB_TOKEN` - Your GitHub personal access token
   - `DEEPSEEK_API_KEY` - Your DeepSeek API key
   - `GITHUB_WEBHOOK_SECRET` - Random secret string (generate with `openssl rand -hex 32`)

## Let us not configure webhook !! 

## Local Testing

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Test the flow:
```bash
python test_full_flow.py
```
