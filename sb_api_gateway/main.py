import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from app.routers import router

logger = logging.getLogger(__name__)

URLs = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
    "http://localhost:8004",
    "http://localhost:8005",
    "http://localhost:8006",
    "http://localhost:8007",
    "http://localhost:8008"
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Project has been launched")

app = FastAPI(
    title="API Gateway",
    description="Единая точка входа для всех микросервисов",
    version="1.0.0",
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=URLs,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"]
)

# app.add_middleware(AuthMiddleware)
# app.add_middleware(RateLimitMiddleware)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "API Gateway",
        "version": "1.0.0",
        "services": ["users", "products", "vacancies", "services"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=settings.DEBUG)
