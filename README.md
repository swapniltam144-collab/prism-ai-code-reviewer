# DeepSeek AI Code Reviewer

An AI-powered code review system that automatically reviews GitHub pull requests using DeepSeek's AI model.

## Features

- 🤖 **AI-Powered Reviews**: Uses DeepSeek AI to analyze code changes
- 📝 **Line-Specific Feedback**: Provides detailed, line-by-line code review comments
- 🔄 **GitHub Integration**: Automatically triggered by GitHub webhooks
- ⚡ **Fast & Efficient**: Quick analysis and feedback on pull requests

## Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd prism-ai-code-reviewer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn httpx python-dotenv pydantic
```

### 4. Configure Environment Variables
```bash
cp environment.env.template environment.env
```

Edit `environment.env` and add your API keys:
```env
GITHUB_TOKEN=your_github_personal_access_token
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 5. Run the Application
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Set Up GitHub Webhook
1. Go to your repository → Settings → Webhooks → Add webhook
2. **Payload URL**: `http://your-server:8000/webhook/github`
3. **Content type**: `application/json`
4. **Events**: Select "Pull requests"
5. Save the webhook

## API Keys Required

### GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` permissions
3. Copy the token (starts with `ghp_`)

### DeepSeek API Key
1. Sign up at [DeepSeek Platform](https://platform.deepseek.com/)
2. Generate an API key
3. Copy the key (starts with `sk-`)

## Usage

Once configured, the system will automatically:
1. Receive webhook events when PRs are opened/updated
2. Fetch the changed files from GitHub
3. Send code diffs to DeepSeek AI for analysis
4. Post intelligent review comments back to the PR

## Testing

Test the webhook locally:
```bash
python test_deepseek.py
```

## Architecture

- **FastAPI**: Web framework for webhook endpoints
- **DeepSeek AI**: AI model for code analysis
- **GitHub API**: Integration with GitHub repositories
- **Async Processing**: Efficient handling of multiple requests

## Security

- Environment variables are used for sensitive data
- API keys are never committed to the repository
- GitHub webhook signatures can be validated (optional)