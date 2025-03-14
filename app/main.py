from fastapi.middleware import cors
from app.api.api import api_router
# from .api.api import api_router
from app.core.config import Settings
from fastapi import FastAPI
from app.core.db import engine, Base
settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.all_cors_origins:
    app.add_middleware(
        cors,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix=settings.API_V1_STR)

