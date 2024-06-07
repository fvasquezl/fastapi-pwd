from typing import Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from app.api.v1.models.user import DBUser
from app.core.config import settings
from app.api.schemas.user import User
from sqlalchemy.orm import Session
from app.api.schemas.token import TokenData
from app.core.database import get_db
from app.core.hashing import Hasher
import pytz

# crear clase que devuelva el la zona horaria

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token")


def authenticate_user(db, username: str, password: str):
    db_user = db.query(DBUser).filter(DBUser.username == username).first()
    if not db_user:
        return False
    if not Hasher.verify_password(password, db_user.hashed_password):
        return False
    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.timezone(settings.TIMEZONE)) + expires_delta
    else:
        expire = datetime.now(pytz.timezone(settings.TIMEZONE)) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print(token_data)
    except jwt.InvalidTokenError:
        raise credentials_exception
    db_user = db.query(DBUser).filter(DBUser.username == token_data.username).first()
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
