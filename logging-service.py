from fastapi import FastAPI
from typing import Dict

LOGGING_SERVICE_PORT = 8001

# Logging Service
logging_app = FastAPI()
log_storage: Dict[str, str] = {}

@logging_app.post("/log")
async def log_message(data: Dict[str, str]):
    msg_id = data.get("id")
    msg = data.get("msg")
    if msg_id and msg:
        log_storage[msg_id] = msg
        print(f"Logged: {msg}")
    return {"status": "success"}

@logging_app.get("/logs")
async def get_logs():
    return {"messages": list(log_storage.values())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(logging_app, host="0.0.0.0", port=LOGGING_SERVICE_PORT)
