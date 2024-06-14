from typing import List, Optional
from fastapi import HTTPException
from pydantic import BaseModel

from app.api.v1.models.category import DBCategory
from sqlalchemy.orm import Session
from slugify import slugify


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    slug: str

    class Config:
        from_attributes = True


def all_db_categories(skip, limit: int, db: Session) -> List[DBCategory]:
    try:
        db_categories = db.query(DBCategory).offset(skip).limit(limit).all()
        return db_categories
    except Exception as e:
        db.rollback()
        raise e


def create_db_category(category: CategoryCreate, db: Session) -> DBCategory:
    try:
        slug = slugify(category.name)
        db_category = DBCategory(**category.model_dump(exclude_none=True))
        db_category.slug = slug
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise e


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
