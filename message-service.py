from fastapi import FastAPI

MESSAGES_SERVICE_PORT = 8002

messages_app = FastAPI()

@messages_app.get("/message")
async def get_static_message():
    return {"message": "Hello, I'm a static message!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(messages_app, host="0.0.0.0", port=MESSAGES_SERVICE_PORT)
