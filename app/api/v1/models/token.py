from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

if TYPE_CHECKING:
    from app.api.v1.models.user import DBUser
else:
    DBUser = "DBUser"
from app.core.database import Base


class DBToken(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    access_token: Mapped[str] = mapped_column(String, unique=True, index=True)
    token_type: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    owner: Mapped[DBUser] = relationship(back_populates="tokens")
