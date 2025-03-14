from fastapi import APIRouter

from app.api.routers import auth, post

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(post.router, tags=["post"])