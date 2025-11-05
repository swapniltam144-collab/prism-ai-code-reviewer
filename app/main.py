from fastapi import FastAPI
from .github_webhook import router as github_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="AI Code Review System")

app.include_router(github_router)

@app.get("/")
def root():
    return {"message": "AI Code Review System is running 🚀"}
