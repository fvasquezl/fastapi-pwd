import re
from typing import List
from fastapi import HTTPException, status
from pydantic import BaseModel, computed_field, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1.models.category import DBCategory


class CategoryBase(BaseModel):
    name: str

    @computed_field
    @property
    def slug(self) -> str:
        return self.slugify(self.name)

    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text

    # @field_validator("name", mode="before")
    # def name_must_be_unique(cls, v, **kwargs):
    #     db: Session = kwargs.get("db")
    #     if db:
    #         if db.query(DBCategory).filter(DBCategory.name == v).first():
    #             raise ValueError("Category name already exists.")
    #     return v


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


def all_db_categories(skip, limit: int, db: Session) -> List[DBCategory]:
    try:
        db_categories = db.query(DBCategory).offset(skip).limit(limit).all()
        print(db_categories)
        return db_categories
    except Exception as e:
        db.rollback()
        raise e


def create_db_category(category: CategoryCreate, db: Session) -> DBCategory:
    try:
        # Verificar si la categoría ya existe
        db_category = (
            db.query(DBCategory).filter(DBCategory.name == category.name).first()
        )
        if db_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists.",
            )
        # slug = slugify(category.name)
        new_db_category = DBCategory(**category.model_dump(exclude_none=True))
        # db_category.slug = slug
        db.add(new_db_category)
        db.commit()
        db.refresh(new_db_category)
        return new_db_category
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e


def read_db_category(category_id: int, db: Session) -> DBCategory:
    db_category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


def update_db_category(
    category_id: int, category: CategoryCreate, db: Session
) -> DBCategory:

    db_category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_db_category(category_id: int, db: Session):
    db_category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category
