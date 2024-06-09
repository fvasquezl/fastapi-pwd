from typing import Union
from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Token(TokenBase):
    id: int
