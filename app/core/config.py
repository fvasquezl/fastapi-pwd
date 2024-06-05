from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Mi Proyecto CRUD"
    API_V1_STR: str = "/api/v1"

    # Configuración del servidor
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # Configuración de la base de datos
    DATABASE_URL: str = "sqlite:///./db.sqlite3"

    # Configuración de seguridad
    SECRET_KEY: str  # openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Timezone
    TIMEZONE: str = "America/Tijuana"

    class Config:
        env_file = ".env"


settings = Settings()
