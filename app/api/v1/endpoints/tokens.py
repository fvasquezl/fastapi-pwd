from typing import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemas.token import Token

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.oauth2 import create_db_token, refresh_db_token


router = APIRouter()


@router.post("/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    db_token = create_db_token(form_data, db)

    return db_token


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db),
):
    db_token = refresh_db_token(refresh_token, db)
    return db_token


# @router.post("/revoke")
# def revoke_token(token: str = Depends(oauth2_scheme)):
#     # ... lógica para invalidar el token ...


# @router.post("/refresh")
# def refresh_token(refresh_token: str = Depends(refresh_token_scheme)):
#     # ... lógica para validar el token de refresco y generar un nuevo token de acceso ...
#     # ... devuelve el nuevo token de acceso ...
