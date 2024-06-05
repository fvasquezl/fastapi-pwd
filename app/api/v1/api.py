from fastapi import APIRouter
from app.api.v1.endpoints import tokens, users

api_router = APIRouter()
api_router.include_router(tokens.router, prefix="/token", tags=["Tokens"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
