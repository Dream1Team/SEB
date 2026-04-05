from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.services.auth_service import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/google/login")
async def google_login(request: Request):
    """Авторизация через Google"""
    result = await user_service.google_login(request)
    return RedirectResponse(url=result.get("auth_url"))


@router.get("/google/callback")
async def google_callback(request: Request):
    """Callback от Google"""
    result = await user_service.google_callback(request)
    return JSONResponse(content=result)