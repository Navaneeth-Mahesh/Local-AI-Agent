from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from app.core.middleware import log_requests
from app.api.routes.settings import router as settings_router
from app.api.routes.ai_provider import (router as ai_provider_router,)
app.include_router(ai_provider_router
                   )
app = FastAPI(
    title="Local AI Agent API",
)
app.middleware("http")("log_request")
app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {
        "message" : "AI Agent Backend !"
    }

app.include_router(settings_router)
