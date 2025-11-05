import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def analyze_code(file_name: str, patch: str) -> list:
    """
    Analyze a single file diff using an AI model.
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text_output = response.choices[0].message.content.strip()

    # Defensive: handle non-JSON outputs
    try:
        import json
        return json.loads(text_output)
    except Exception:
        return [{"line": 1, "severity": "info", "comment": text_output}]
