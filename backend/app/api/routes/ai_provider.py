from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.ai_provider import (
    AIProviderCreate,
    AIProviderResponse,
)
from app.services.ai_provider_service import (
    AIProviderService,
)

router = APIRouter(
    prefix="/ai-provider",
    tags=["AI Provider"],
)


@router.get(
    "/",
    response_model=AIProviderResponse,
)
def get_provider(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AIProviderService(db).get_provider(
        current_user.id
    )


@router.post(
    "/",
    response_model=AIProviderResponse,
)
def save_provider(
    data: AIProviderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return AIProviderService(db).save_provider(
        current_user.id,
        data,
    )