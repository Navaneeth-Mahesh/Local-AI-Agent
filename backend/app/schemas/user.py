from pydantic import BaseModel, ConfigDict


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: str

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
    email: Email

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str