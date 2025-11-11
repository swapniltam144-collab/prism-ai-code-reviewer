from fastapi import FastAPI
from .github_webhook import router as github_router
from dotenv import load_dotenv
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI(title="AI Code Review System")

app.include_router(github_router)

@app.get("/")
async def root():
    return {
        "message": "AI Code Review System is running 🚀",
    }
 