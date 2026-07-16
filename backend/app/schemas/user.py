from pydantic import BaseModel, ConfigDict

from app.core.validators import (
    Username,
    Password,
    Email,
)


class UserRegister(BaseModel):
    username: Username
    email: Email
    password: Password


class UserLogin(BaseModel):
    email: Email
    password: Password


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str