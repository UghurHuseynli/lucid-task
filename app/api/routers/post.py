from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.db.user import UserModel
from app.crud.crud import (
    create_post, get_user_posts, get_post, delete_post,
    get_cached_posts, update_posts_cache
)
from app.schemas.post import PostCreate, Post, PostList, PostDelete
from app.api.routers.auth import get_current_user

router = APIRouter(tags=["posts"])

@router.post("/posts", response_model=dict)
async def add_post(
    post: PostCreate = Body(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create new post
    db_post = create_post(db, post, current_user.id)
    
    return {"post_id": db_post.id}

@router.get("/posts", response_model=PostList)
async def get_posts(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if we have cached data for this user
    cached_posts = get_cached_posts(current_user.id)
    if cached_posts is not None:
        return {"posts": cached_posts}
    
    # Retrieve posts from database
    db_posts = get_user_posts(db, current_user.id)
    
    # Convert to Pydantic models
    posts = [Post.from_orm(post) for post in db_posts]
    
    # Update cache
    update_posts_cache(current_user.id, posts)
    
    return {"posts": posts}

@router.delete("/posts", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_post(
    post_data: PostDelete,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the post
    db_post = get_post(db, post_data.post_id, current_user.id)
    
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or access denied",
        )
    
    # Delete the post
    delete_post(db, db_post)