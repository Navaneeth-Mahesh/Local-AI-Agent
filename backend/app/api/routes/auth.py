from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_auth_service
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserRegister,
    service: AuthService = Depends(get_auth_service),
):
    return await service.register_user(user)


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    credentials: UserLogin,
    service: AuthService = Depends(get_auth_service),
):
    return await service.login_user(credentials)


@router.post(
    "/refresh",
    response_model=Token,
)
async def refresh_token(
    refresh_token: str,
    service: AuthService = Depends(get_auth_service),
):
    return await service.refresh_access_token(refresh_token)