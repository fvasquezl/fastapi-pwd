from datetime import datetime
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.ext.declarative import AbstractConcreteBase
from app.core.config import settings

# Crear el motor de la base de datos
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a declarative database
class Base(DeclarativeBase):
    pass


class NotFoundError(Exception):
    pass


# Timestamp abstract class
class TimeStampedModel(AbstractConcreteBase, Base):
    created_at = mapped_column(DateTime(timezone=True), default=datetime.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=datetime.now())


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
