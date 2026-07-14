from sqlalchemy.orm import Session
from app.core.security import (
        hash_password,
        verify_password,
        create_access_token,
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
            raise ValueError(
                "Email already registered."
            )
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
    ) -> str:
        user = self.repository.get_by_email(
            data.email
        )
        if not user:
            raise ValueError(
                "Invalid credentials."
            )
        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid credentials."
            )
        return create_access_token(
            user.id
        )