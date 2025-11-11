import httpx
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

async def fetch_pr_files(owner: str, repo: str, pr_number: int):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def post_pr_comment(owner: str, repo: str, pr_number: int, body: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json={"body": body})
        response.raise_for_status()
        return response.json()

async def fetch_pull_request(owner: str, repo: str, pr_number: int):
    """Fetch PR details, including head/base commits if needed."""
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()

async def create_pull_request_review(owner: str, repo: str, pr_number: int, comments: list):
    """Create a PR review with inline comments.

    comments: List of dicts with keys { path, position, body }
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    payload = {
        "event": "COMMENT",
        "comments": comments
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
 