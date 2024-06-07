from datetime import timedelta
from typing import Optional
from fastapi import Depends
from pydantic import BaseModel, EmailStr

from app.api.v1.models.token import DBToken
from app.core.database import get_db
from sqlalchemy.orm import Session


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None


def create_db_token(
    user_id: int,
    access_token: str,
    expires_delta: timedelta | None = None,
    db: Session = Depends(get_db),
) -> Token:
    # Guarda el token en la base de datos
    db_token = DBToken(
        access_token=access_token,
        token_type="bearer",
        user_id=user_id,
        expires_at=expires_delta,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
