import httpx
import json

# Mock GitHub webhook payload
mock_payload = {
    "action": "opened",
    "pull_request": {
        "number": 1,
        "title": "Test PR",
        "user": {"login": "testuser"}
    },
    "repository": {
        "name": "test-repo",
        "owner": {"login": "test-owner"},
        "full_name": "test-owner/test-repo"
    }
}

def test_webhook():
    """Send a mock webhook to your local server"""
    url = "http://localhost:8000/webhook/github"
    
    print("Sending mock webhook to local server...")
    print(f"Payload: {json.dumps(mock_payload, indent=2)}\n")
    
    try:
        response = httpx.post(url, json=mock_payload, timeout=30.0)
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except httpx.ConnectError:
        print("❌ Error: Could not connect to server.")
        print("Make sure the server is running: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_webhook()
