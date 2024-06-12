import re
from typing import Optional
from pydantic import BaseModel, Field, ValidationInfo, field_validator


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    slug: Optional[str]

    @field_validator("title", mode="before")
    def generate_slug(cls, v: str, info: ValidationInfo) -> str:
        if v:
            return cls.slugify(v)
        return None

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
    slug: Optional[str] = Field(None, min_length=3, max_length=100)


class Post(PostBase):
    id: int
    user_id: int
    slug: str = Field(..., min_length=3, max_length=1000)

    class Config:
        from_attributes = True


# https://medium.com/@khalil.saidane/scalabel-fastapi-project-layered-architecture-10852a40fd38
