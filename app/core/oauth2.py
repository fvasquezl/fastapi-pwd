from typing import Annotated
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from app.api.v1.models.token import DBToken
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
    except jwt.InvalidTokenError:
        raise credentials_exception

    db_user = db.query(DBUser).filter(DBUser.username == token_data.username).first()
    if db_user is None:
        raise credentials_exception
    return db_user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):

    if current_user.is_disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_db_token(form_data, db):
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.now(pytz.timezone("America/Tijuana")) + access_token_expires
    existing_token = db.query(DBToken).filter(DBToken.user_id == db_user.id).first()
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )

    if existing_token:
        existing_token.access_token = access_token
        existing_token.expires_at = expires_at
        db.commit()
        db.refresh(existing_token)
        return existing_token
    else:
        # Guarda el token en la base de datos
        db_token = DBToken(
            access_token=access_token,
            token_type="bearer",
            user_id=db_user.id,
            expires_at=expires_at,
        )
        db.add(db_token)
        db.commit()
        db.refresh(db_token)

        return db_token
