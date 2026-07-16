from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
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
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register_user(user)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.login_user(credentials)


@router.post(
    "/refresh",
    response_model=Token,
)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.refresh_access_token(refresh_token)