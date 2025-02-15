from fastapi import FastAPI, HTTPException, Request
import uuid
import httpx

FACADE_SERVICE_PORT = 8000
LOGGING_SERVICE_URL = "http://localhost:8001"
MESSAGES_SERVICE_URL = "http://localhost:8002"

facade_app = FastAPI()

@facade_app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    msg = data.get("msg")
    if not msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    msg_id = str(uuid.uuid4())
    async with httpx.AsyncClient() as client:
        await client.post(f"{LOGGING_SERVICE_URL}/log", json={"id": msg_id, "msg": msg})
    
    return {"uuid": msg_id, "message": msg}

@facade_app.get("/get")
async def get_messages():
    async with httpx.AsyncClient() as client:
        log_response = await client.get(f"{LOGGING_SERVICE_URL}/logs")
        msg_response = await client.get(f"{MESSAGES_SERVICE_URL}/message")
    
    if log_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get logs")
    if msg_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get static message")
    
    logs = log_response.json().get("messages", [])
    static_message = msg_response.json().get("message", "")
    
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    if not static_message:
        raise HTTPException(status_code=404, detail="No static message found")
    
    return {"logs": logs, "static_message": static_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(facade_app, host="0.0.0.0", port=FACADE_SERVICE_PORT)
