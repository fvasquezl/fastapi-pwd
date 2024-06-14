from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.models.category import DBCategory
from app.api.schemas.category import (
    CategoryCreate,
    Category,
    all_db_categories,
    create_db_category,
    read_db_category,
    update_db_category,
    delete_db_category,
)
from app.core.database import get_db

router = APIRouter()


# Get all Categories
@router.get("/", response_model=list[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_categories = all_db_categories(skip, limit, db)
    return db_categories


# CREATE a Category
@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = create_db_category(category, db)
    return Category(**db_category.__dict__)


# READ a Category
@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = read_db_category(category_id, db)
    return Category(**db_category.__dict__)


# UPDATE a Category
@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int, category: CategoryCreate, db: Session = Depends(get_db)
):
    db_category = update_db_category(category_id, category, db)
    return Category(**db_category.__dict__)


# DELETE a Category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = delete_db_category(category_id, db)
    return Category(**db_category.__dict__)
