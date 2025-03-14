from pydantic import BaseModel, EmailStr, field_validator, constr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(description="User's email address", example="user@example.com")
    
    @field_validator('email')
    def email_must_be_valid(cls, v):
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

class UserCreate(UserBase):
    password: str = Field(
        description="User's password (8-100 characters)",
        example="SecureP@ssw0rd"
    )
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")

class TokenData(BaseModel):
    user_id: Optional[int] = None