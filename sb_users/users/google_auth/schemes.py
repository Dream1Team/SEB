from pydantic import BaseModel
from typing import Optional


class GoogleUserInfo(BaseModel):
    email: str
    given_name: str
    family_name: str
    picture: Optional[str] = None
    sub: str  # Google ID
    email_verified: bool = True