from fastapi import APIRouter, Request


router = APIRouter(prefix="/chats")


@router.post('/join_chat', summary="Подключение к чату")
async def join_chat(request: Request, user_id: int, room_id: int):
    username = ...
    return {"request": request,
            "user_id": user_id,
            "username": username,
            "room_id": room_id}