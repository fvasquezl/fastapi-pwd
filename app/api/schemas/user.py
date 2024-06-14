from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.hashing import Hasher


class UserBase(BaseModel):
    username: str = Field(min_length=5, default="username")
    email: EmailStr | None = Field(default=None)


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

        # Desactiva la validación de campos requeridos
        arbitrary_types_allowed = True

        # Define el constructor para asignar los valores correctamente

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.id = data.get("id")
        self.is_disabled = data.get("is_disabled")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
