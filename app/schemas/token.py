from typing import Optional

from pydantic import BaseModel

from .user import AuthUser


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: Optional[str] = None
    sub: Optional[int] = None
    user: Optional[AuthUser] = None
