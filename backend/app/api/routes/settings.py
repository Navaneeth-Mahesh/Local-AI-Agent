from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.settings import (
    UserSettingsResponse,
    UserSettingsUpdate,
)
from app.services.settings_service import SettingsService

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get(
    "/",
    response_model=UserSettingsResponse,
)
def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    return service.get_settings(current_user.id)


@router.put(
    "/",
    response_model=UserSettingsResponse,
)
def update_settings(
    data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = SettingsService(db)

    return service.update_settings(
        current_user.id,
        data,
    )