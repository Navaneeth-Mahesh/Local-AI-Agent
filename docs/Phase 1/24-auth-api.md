# Phase 1 — Lesson 20: Building the Authentication API (FastAPI Routes)

Congratulations! You're about to complete your **first end-to-end backend feature**.

After this lesson, your backend will be able to:

* Register users
* Login users
* Generate JWT tokens
* Protect routes
* Return the currently authenticated user

This is the same pattern we'll use for **Chats**, **Memory**, **Documents**, **Settings**, and **AI Tools**.

---

# Goal

By the end of this lesson, you'll have:

```text
app/
├── api/
│   ├── routes/
│   │   ├── auth.py
│   │   └── users.py
│   └── dependencies.py
│
├── services/
│   └── auth_service.py
│
├── repositories/
│   └── user_repository.py
│
└── schemas/
    └── user.py
```

working together.

---

# Big Picture

Until now we built these layers separately.

Today we connect them.

```text
             Browser

                │

      POST /auth/register

                │

        FastAPI Route

                │

        AuthService

                │

      UserRepository

                │

          PostgreSQL
```

This is called the **Request Pipeline**.

---

# Step 1 — Create the Auth Router

Create:

```text
app/api/routes/auth.py
```

Imports:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    Token,
)
from app.services.auth_service import AuthService
```

---

# What is APIRouter?

Instead of putting everything inside `main.py`

Bad:

```python
@app.post(...)
@app.post(...)
@app.get(...)
@app.delete(...)
```

Professional projects group related endpoints.

Example:

```text
/auth

/users

/chat

/documents

/settings
```

Each gets its own router.

---

Create the router.

```python
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
```

Now every endpoint automatically begins with:

```text
/auth
```

Example

```text
POST /auth/register

POST /auth/login
```

---

# Step 2 — Register Endpoint

Let's design it first.

Input

```json
{
    "username":"Nav",
    "email":"nav@gmail.com",
    "password":"secret"
}
```

↓

Service

↓

Repository

↓

Database

↓

Return

```json
{
    "id":1,
    "username":"Nav",
    "email":"nav@gmail.com"
}
```

---

Implementation

```python
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

    try:
        return service.register_user(user)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
```

---

# Understanding Every Line

---

## `response_model`

```python
response_model=UserResponse
```

FastAPI automatically converts

```python
User
```

↓

```json
{
    "id":1,
    "username":"Nav",
    "email":"nav@gmail.com"
}
```

using your schema.

---

## Why `Depends(get_db)`?

Remember Lesson 11.

Instead of

```python
SessionLocal()
```

FastAPI injects a database session.

Each request gets:

```text
Open Session

↓

Use Session

↓

Close Session
```

Automatically.

---

## Why `HTTPException` Here?

Notice.

Service raises:

```python
ValueError
```

API converts it into

```python
HTTPException
```

This is exactly how responsibilities should be divided.

---

# Step 3 — Login Endpoint

Flow

```text
Email

↓

Service

↓

Repository

↓

Verify Password

↓

Create JWT

↓

Return Token
```

Implementation

```python
@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        token = service.login_user(credentials)

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
```

---

# Why Return a Dictionary?

Our schema is

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

So we return

```python
{
    "access_token": "...",
    "token_type": "bearer",
}
```

FastAPI validates it automatically.

---

# Step 4 — Protected Routes

Create

```text
app/api/routes/users.py
```

Imports

```python
from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse
```

---

Create router

```python
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
```

---

Endpoint

```python
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
```

Notice something amazing.

There is:

* No SQL
* No JWT decoding
* No authentication code

Because Dependency Injection already handled it.

---

# Request Flow

Suppose the frontend sends

```http
GET /users/me

Authorization: Bearer TOKEN
```

FastAPI

↓

`OAuth2PasswordBearer`

↓

Extract Token

↓

Verify JWT

↓

Load User

↓

Inject User

↓

Execute Route

The route receives

```python
current_user
```

already authenticated.

---

# Step 5 — Register Routers

Inside

```text
app/main.py
```

```python
from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router

app = FastAPI(
    title="Local AI Agent API",
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "AI Agent Backend!"
    }
```

---

# Swagger Testing

Start the server.

```bash
uvicorn app.main:app --reload
```

Open

```text
http://127.0.0.1:8000/docs
```

---

## Test 1

POST

```text
/auth/register
```

Example

```json
{
  "username": "navaneeth",
  "email": "nav@gmail.com",
  "password": "Password123"
}
```

Expected

```http
201 Created
```

---

## Test 2

POST

```text
/auth/login
```

Example

```json
{
  "email":"nav@gmail.com",
  "password":"Password123"
}
```

Expected

```json
{
  "access_token":"eyJhbGc...",
  "token_type":"bearer"
}
```

---

## Test 3

Click

```text
Authorize
```

Paste

```text
Bearer eyJhbGc...
```

or, if your OpenAPI security scheme is configured, just paste the JWT value.

---

## Test 4

GET

```text
/users/me
```

Expected

```json
{
  "id":1,
  "username":"navaneeth",
  "email":"nav@gmail.com"
}
```

Congratulations.

You have built your first protected API endpoint.

---

# Complete Authentication Pipeline

```text
            Register

Frontend

↓

POST /auth/register

↓

Schema Validation

↓

AuthService

↓

Hash Password

↓

Repository

↓

PostgreSQL

──────────────────────────────

Login

↓

POST /auth/login

↓

Verify Password

↓

Create JWT

↓

Return Token

──────────────────────────────

Protected Request

↓

Authorization Header

↓

OAuth2PasswordBearer

↓

Verify JWT

↓

Load User

↓

Route Executes
```

---

# Common Beginner Mistakes

## ❌ Creating a database session manually inside routes

Always use `Depends(get_db)`.

---

## ❌ Returning SQLAlchemy models directly without response schemas

Use `response_model` so FastAPI validates and serializes the response.

---

## ❌ Putting password verification inside routes

Routes should coordinate the request, not implement business logic.

---

## ❌ Decoding JWT inside every protected endpoint

Centralize authentication in `get_current_user()`.

---

## ❌ Returning different error messages for "email not found" and "wrong password"

Use a generic message like `"Invalid credentials"` to reduce information disclosure.

---

# Architecture We've Built

```text
React Frontend
        │
        ▼
FastAPI Route
        │
        ▼
Pydantic Schema
        │
        ▼
Auth Service
        │
        ▼
User Repository
        │
        ▼
SQLAlchemy
        │
        ▼
PostgreSQL
```

This layered architecture is scalable, testable, and reusable.

---

# Mini Challenge

Answer these without looking back:

1. Why do we use `APIRouter` instead of defining every endpoint in `main.py`?
2. What does `response_model` do?
3. Why is `Depends(get_db)` preferred over creating `SessionLocal()` manually?
4. Why does the API layer convert exceptions into `HTTPException` instead of the Service?
5. What happens internally when a client calls `GET /users/me` with a Bearer token?
6. Why is `current_user` injected into the route instead of being looked up manually?
7. Why do we keep routes "thin" and move business logic into the Service layer?

---

# Phase 1 Milestone

At this stage, you've completed the first complete backend feature using a production-style architecture:

* Configuration management
* Logging
* PostgreSQL
* SQLAlchemy
* Alembic
* Database sessions
* Pydantic schemas
* Repository pattern
* Service layer
* JWT authentication
* Protected routes
* FastAPI routing
* Dependency injection

This is a significant milestone because every future module—chat conversations, AI memory, document indexing, permissions, and tools—will follow this same structure.

## Lesson 21 Preview

Before moving to AI features, we'll strengthen the authentication system by adding:

* Custom exception classes
* Global exception handlers
* Consistent API response format
* Better validation
* Password strength rules
* Username validation
* Cleaner error handling

These improvements will make your backend feel much closer to a production-grade application rather than a tutorial project.
