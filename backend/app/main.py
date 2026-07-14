from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
app = FastAPI(
    title="Local AI Agent API",
)

app.include_router(auth_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {
        "message" : "AI Agent Backend !"
    }
