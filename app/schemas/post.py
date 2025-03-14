from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, field_validator

class PostBase(BaseModel):
    text: str = Field(
        description="Post content (1-1000000 characters)",
        example="This is my first post!"
    )
    
    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Post text cannot be empty')
        return v

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: str
    created_at: datetime
    user_id: int
    
    class Config:
        orm_mode = True

class PostList(BaseModel):
    posts: List[Post]

class PostDelete(BaseModel):
    post_id: str = Field(description="ID of the post to delete", example="123e4567-e89b-12d3-a456-426614174000")