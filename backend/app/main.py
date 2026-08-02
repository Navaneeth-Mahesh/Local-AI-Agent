from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.middleware import log_requests
from app.database.session import engine
from app.database.base import Base
import app.models  # Ensure all SQLAlchemy models are registered

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.settings import router as settings_router
from app.api.routes.ai_provider import router as ai_provider_router
from app.api.routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables if they do not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose of database engine
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)

# Include API Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(settings_router)
app.include_router(ai_provider_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "docs_url": "/docs",
    }