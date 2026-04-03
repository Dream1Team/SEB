import uvicorn
from fastapi import FastAPI

from api import chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    uvicorn.run("main:chat_app", host='localhost', port=8001)