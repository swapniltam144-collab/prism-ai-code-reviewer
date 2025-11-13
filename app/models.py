from pydantic import BaseModel
from typing import Optional, List

class PullRequestPayload(ChildModel):
    action: str
    pull_request: dict
    repository: dict

class ReviewComment(BaseModel):
    file: str
    line: int
    severity: str
    comment: str
