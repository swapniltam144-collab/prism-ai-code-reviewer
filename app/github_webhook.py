from fastapi import APIRouter, Request, HTTPException
from .models import PullRequestPayload
from .github_service import fetch_pr_files, post_pr_comment
from .code_reviewer import analyze_code
import asyncio
import hmac
import hashlib
import os

router = APIRouter()

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify GitHub webhook signature"""
    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    if not secret:
        return True  # Skip verification if no secret set
    
    hash_object = hmac.new(secret.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

@router.post("/webhook/github")
async def github_webhook(payload: PullRequestPayload, request: Request):
    # Verify webhook signature
    signature = request.headers.get("X-Hub-Signature-256", "")
    body = await request.body()
    if not verify_signature(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    if payload.action not in ["opened", "synchronize"]:
        return {"message": "Ignored non-PR-open events."}

    repo_info = payload.repository
    pr = payload.pull_request
    owner = repo_info["owner"]["login"]
    repo = repo_info["name"]
    pr_number = pr["number"]

    # Fetch changed files
    files = await fetch_pr_files(owner, repo, pr_number)

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
