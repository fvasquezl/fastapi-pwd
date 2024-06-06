from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel
from app.core.hashing import Hasher


class UserBase(BaseModel):
    username: str
    email: str | None = None


class UserCreate(UserBase):
    hashed_password: str

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(**kwargs)
        data["hashed_password"] = Hasher.get_password_hash(self.hashed_password)
        return data


class User(UserBase):
    id: int
    is_disabled: bool | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
