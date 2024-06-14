from datetime import datetime
import re
from typing import Any, Optional
from pydantic import BaseModel, Field, computed_field


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=5)

    @computed_field
    @property
    def slug(self) -> str:
        return self.slugify(self.title)

    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text


class PostCreate(PostBase):
    # category_id: int
    pass


class PostUpdate(PostBase):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=10)


class Post(PostBase):
    id: int
    user_id: int
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


# https://medium.com/@khalil.saidane/scalabel-fastapi-project-layered-architecture-10852a40fd38
