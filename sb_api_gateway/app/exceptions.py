from fastapi import HTTPException


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Требуется авторизация"):
        super().__init__(status_code=401, detail=detail)


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Доступ запрещен"):
        super().__init__(status_code=403, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Ресурс не найден"):
        super().__init__(status_code=404, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Неверный запрос"):
        super().__init__(status_code=400, detail=detail)