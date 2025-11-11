from fastapi import APIRouter, Request, HTTPException
from .github_service import fetch_pr_files, create_pull_request_review
from .code_reviewer import analyze_code
import hashlib
import hmac
import os

router = APIRouter()

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")

def verify_signature(request_body: bytes, signature_header: str) -> bool:
    if not GITHUB_WEBHOOK_SECRET:
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    received_sig = signature_header.split("=", 1)[1]
    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=request_body, digestmod=hashlib.sha256)
    expected = mac.hexdigest()
    return hmac.compare_digest(received_sig, expected)

def new_line_to_diff_position(patch: str, new_line: int):
    """Map a line number in the new file to a 1-based position in the unified diff."""
    if not patch:
        return None
    lines = patch.splitlines()
    position = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        position += 1
        if line.startswith("@@"):
            header = line
            # header like: @@ -a,b +c,d @@
            try:
                plus_seg = header.split("+")[1].split("@@")[0].strip()
                if "," in plus_seg:
                    new_start = int(plus_seg.split(",")[0])
                else:
                    new_start = int(plus_seg)
            except Exception:
                new_start = 1
            cur_new = new_start
            i += 1
            while i < len(lines) and not lines[i].startswith("@@"):
                hline = lines[i]
                position += 1
                if hline.startswith(" "):
                    if cur_new == new_line:
                        return position
                    cur_new += 1
                elif hline.startswith("+"):
                    if cur_new == new_line:
                        return position
                    cur_new += 1
                elif hline.startswith("-"):
                    # deletion in old file only; new_line doesn't advance
                    pass
                i += 1
            continue
        i += 1
    return None

@router.post("/webhook/github")
async def github_webhook(request: Request):
    raw = await request.body()
    if not verify_signature(raw, request.headers.get("X-Hub-Signature-256", "")):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    action = payload.get("action")
    if action not in ["opened", "reopened", "synchronize", "ready_for_review"]:
        return {"message": f"Ignored action: {action}"}

    repo_info = payload["repository"]
    pr = payload["pull_request"]
    owner = repo_info["owner"]["login"]
    repo = repo_info["name"]
    pr_number = pr["number"]

    files = await fetch_pr_files(owner, repo, pr_number)
    inline_comments = []

    for f in files:
        patch = f.get("patch")
        if not patch:
            continue
        ai_feedback = await analyze_code(f["filename"], patch)
        for c in ai_feedback:
            target_line = c.get("line")
            if not isinstance(target_line, int):
                continue
            position = new_line_to_diff_position(patch, target_line)
            if position is None:
                continue
            body = f"{c.get('comment','')}\n\n(severity: {c.get('severity','info')})"
            inline_comments.append({
                "path": f["filename"],
                "position": position,
                "body": body
            })

    if not inline_comments:
        return {"status": "No inline comments to post"}

    await create_pull_request_review(owner, repo, pr_number, inline_comments)
    return {"status": "Inline review posted", "count": len(inline_comments)}
 