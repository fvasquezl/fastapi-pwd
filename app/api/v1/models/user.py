from typing import List
from sqlalchemy import Integer, String, Boolean
from app.api.v1.models.token import DBToken
from app.core.database import TimeStampedModel
from sqlalchemy.orm import relationship, Mapped, mapped_column


class DBUser(TimeStampedModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_disabled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relacion con Post
    tokens: Mapped[List[DBToken]] = relationship(back_populates="owner")
