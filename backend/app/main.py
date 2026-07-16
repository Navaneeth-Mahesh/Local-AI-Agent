from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.settings import router as settings_router
from app.api.routes.ai_provider import router as ai_provider_router
from app.core.middleware import log_requests

app = FastAPI(
    title="Local AI Agent API",
)

app.middleware("http")(log_requests)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(settings_router)
app.include_router(ai_provider_router)


@app.get("/")
def root():
    return {
        "message": "AI Agent Backend!"
    }
