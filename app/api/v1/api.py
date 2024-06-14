from fastapi import APIRouter
from app.api.v1.endpoints import tokens, users, posts, categories
from app.core.database import Base, engine


api_router = APIRouter()
api_router.include_router(tokens.router, prefix="/token", tags=["Tokens"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(posts.router, prefix="/posts", tags=["Posts"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Crea la base de datos desde los modelos
Base.metadata.create_all(bind=engine)
