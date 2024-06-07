from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import pytz

from app.api.schemas.token import Token
from app.api.v1.models.token import DBToken
from app.core.config import settings
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.oauth2 import authenticate_user, create_access_token


router = APIRouter()


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    expires_at = datetime.now(pytz.timezone("America/Tijuana")) + access_token_expires
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

    return Token(access_token=access_token, token_type="bearer")


# @router.post("/refresh")
# def refresh_token(refresh_token: str = Depends(oauth2_scheme)):
#     # ... lógica para validar el token de refresco y generar un nuevo token de acceso ...


# @router.post("/revoke")
# def revoke_token(token: str = Depends(oauth2_scheme)):
#     # ... lógica para invalidar el token ...


# @router.post("/refresh")
# def refresh_token(refresh_token: str = Depends(refresh_token_scheme)):
#     # ... lógica para validar el token de refresco y generar un nuevo token de acceso ...
#     # ... devuelve el nuevo token de acceso ...
