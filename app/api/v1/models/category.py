from typing import List
from sqlalchemy import Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.api.v1.models.post import DBPost


class DBCategory(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String)

    # Relación
    posts: Mapped[List[DBPost]] = relationship(back_populates="category")
