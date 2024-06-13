from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True
    )
