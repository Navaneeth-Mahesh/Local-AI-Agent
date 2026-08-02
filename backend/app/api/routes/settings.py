from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, get_settings_service
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
async def get_settings(
    current_user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
):
    return await service.get_settings(current_user.id)


@router.put(
    "/",
    response_model=UserSettingsResponse,
)
async def update_settings(
    data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    service: SettingsService = Depends(get_settings_service),
):
    return await service.update_settings(
        current_user.id,
        data,
    )