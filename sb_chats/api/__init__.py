from fastapi import APIRouter

from api.router_socket import router as socket_router
from api.router import router as connect_router


chat_router = APIRouter()

chat_router.include_router(socket_router)
chat_router.include_router(connect_router)