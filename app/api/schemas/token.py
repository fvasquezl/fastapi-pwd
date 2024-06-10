from typing import Union
from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class TokenRefresh(BaseModel):
    refresh_token: str


class Token(TokenBase):
    id: int
