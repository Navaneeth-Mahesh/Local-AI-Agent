from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserRegister,
    UserLogin,
)


class AuthService:
    def __init__(
        self,
        db: Session,
    ):
        self.repository = UserRepository(db)

    def register_user(
        self,
        data: UserRegister,
    ) -> User:
        existing = self.repository.get_by_email(
            data.email
        )
        if existing:
            raise EmailAlreadyExistsException()

        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
        )
        return self.repository.create(user)

    def login_user(
        self,
        data: UserLogin,
    ) -> dict:
        user = self.repository.get_by_email(
            data.email
        )
        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise InvalidCredentialsException()

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "token_type": "bearer",
        }

    def refresh_access_token(
        self,
        refresh_token: str,
    ) -> dict:
        payload = verify_token(
            refresh_token,
            "refresh",
        )

        if not payload:
            raise InvalidCredentialsException()

        return {
            "access_token": create_access_token(
                int(payload["sub"])
            ),
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }