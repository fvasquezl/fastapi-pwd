from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.schemas.post import Post, PostCreate
from app.api.schemas.user import User
from app.api.v1.models.post import DBPost
from app.core.database import get_db
from app.core.oauth2 import get_current_user

router = APIRouter()


@router.post("/", response_model=Post)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = DBPost(**post.model_dump())
    db_post.user_id = current_user.id
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


# Get all post from user
@router.get("/{user_id}/posts", response_model=list[Post])
def read_post(user_id: int, db: Session = Depends(get_db)):
    db_posts = db.query(DBPost).filter(DBPost.user_id == user_id).all()
    if not db_posts:
        raise HTTPException(status_code=404, detail="Post not found for this user")
    return db_posts
