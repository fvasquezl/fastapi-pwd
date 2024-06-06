from fastapi import APIRouter
from app.api.v1.endpoints import tokens, users
from app.core.database import Base, engine


api_router = APIRouter()
api_router.include_router(tokens.router, prefix="/token", tags=["Tokens"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Crea la base de datos desde los modelos
Base.metadata.create_all(bind=engine)
