from fastapi import APIRouter, Request
from .models import PullRequestPayload
from .github_service import fetch_pr_files, post_pr_comment
from .code_reviewer import analyze_code
import asyncio

router = APIRouter()

@router.post("/webhook/github")
async def github_webhook(payload: PullRequestPayload, request: Request):
    if payload.action not in ["opened", "synchronize"]:
        return {"message": "Ignored non-PR-open events."}

    repo_info = payload.repository
    pr = payload.pull_request
    owner = repo_info["owner"]["login"]
    repo = repo_info["name"]
    pr_number = pr["number"]

    # Fetch changed files
    files = await fetch_pr_files(owner, repo, pr_number)
    print(files)
    review_comments = []

    for f in files:
        if not f.get("patch"):
            continue
        ai_feedback = await analyze_code(f["filename"], f["patch"])
        for c in ai_feedback:
            review_comments.append({
                "file": f["filename"],
                "line": c.get("line", 0),
                "severity": c.get("severity", "info"),
                "comment": c.get("comment", "")
            })

    # Format feedback as PR comment
    from .github_service import post_review_summary

    await post_review_summary(owner, repo, pr_number, review_comments)
    
    return {"status": "AI review posted", "count": len(review_comments)}
