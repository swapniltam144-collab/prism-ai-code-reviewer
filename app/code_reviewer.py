import os
import json
import httpx

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

async def analyze_code(file_name: str, patch: str) -> list:
    """
    Analyze a single file diff using DeepSeek AI model.
    Returns a list of structured comments.
    """
    prompt = f"""
    You are a senior code reviewer.
    Review the following diff from `{file_name}` and provide detailed, line-specific feedback.

    Respond in JSON list format like:
    [
      {{
        "line": 42,
        "severity": "medium",
        "comment": "Consider handling null values before using user.name"
      }}
    ]

    Code Diff:
    {patch}
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    text_output = data["choices"][0]["message"]["content"].strip()

    # Defensive: handle non-JSON outputs
    try:
        # Remove markdown code blocks if present
        if text_output.startswith("```json"):
            text_output = text_output.replace("```json", "").replace("```", "").strip()
        elif text_output.startswith("```"):
            text_output = text_output.replace("```", "").strip()
        
        return json.loads(text_output)
    except Exception as e:
        return [{"line": 1, "severity": "info", "comment": text_output}]
