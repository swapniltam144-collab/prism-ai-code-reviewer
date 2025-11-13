from fastapi import FastAPI, Request, HTTPException
from .github_webhook import router as github_router
from dotenv import load_dotenv
import logging
import json

load_dotenv()  # call this if you want dotenv to load env vars

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Code Review System")

app.include_router(github_router)

@app.get("/")
def root():
    return {"message": "AI Code Review System is running 🚀"}

@app.post("/health")
async def get_info(request: Request):
    """
    Reads the request body as JSON, logs it to stdout, and returns it.
    If the body is not valid JSON, returns a 400 error.
    """
    try:
        payload = await request.json()
    except Exception:
        # Could not parse JSON — return a helpful error
        text = await request.body()
        logger.warning("Received non-JSON body: %s", text[:200])
        raise HTTPException(status_code=400, detail="Request body must be valid JSON")

    # Log the payload (prints to the console where uvicorn is running)
    logger.info("🔔 Webhook received: %s", json.dumps(payload, indent=2))

    # Optional: do whatever processing you need here (enqueue job, call review logic, etc.)

    return {
        "message": "AI Code Review 1 System is running 🚀",
        "received": payload
    }
