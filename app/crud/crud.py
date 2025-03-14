import time
from typing import List, Optional
from sqlalchemy.orm import Session

from app.db.user import UserModel, PostModel
from app.schemas.auth import UserCreate
from app.schemas.post import PostCreate, Post
from app.core.config import POSTS_CACHE, CACHE_TTL_SECONDS

# User CRUD operations
def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user: UserCreate, hashed_password: str) -> UserModel:
    db_user = UserModel(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Post CRUD operations
def create_post(db: Session, post: PostCreate, user_id: int) -> PostModel:
    db_post = PostModel(text=post.text, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Invalidate user's cache
    invalidate_user_cache(user_id)
    
    return db_post

def get_user_posts(db: Session, user_id: int) -> List[PostModel]:
    return db.query(PostModel).filter(PostModel.user_id == user_id).all()

def get_post(db: Session, post_id: str, user_id: int) -> Optional[PostModel]:
    return db.query(PostModel).filter(
        PostModel.id == post_id, 
        PostModel.user_id == user_id
    ).first()

def delete_post(db: Session, post: PostModel) -> None:
    user_id = post.user_id
    db.delete(post)
    db.commit()
    
    # Invalidate user's cache
    invalidate_user_cache(user_id)

# Cache operations
def get_cached_posts(user_id: int) -> Optional[List[Post]]:
    if user_id in POSTS_CACHE:
        cache_entry = POSTS_CACHE[user_id]
        # Check if cache is still valid (not expired)
        if time.time() - cache_entry["timestamp"] < CACHE_TTL_SECONDS:
            return cache_entry["data"]
    return None

def update_posts_cache(user_id: int, posts: List[Post]) -> None:
    POSTS_CACHE[user_id] = {
        "data": posts,
        "timestamp": time.time()
    }

def invalidate_user_cache(user_id: int) -> None:
    if user_id in POSTS_CACHE:
        del POSTS_CACHE[user_id]