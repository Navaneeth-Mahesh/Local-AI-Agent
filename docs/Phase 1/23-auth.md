# Phase 1 — Lesson 19: Building the Authentication Service (Business Logic)

Welcome to one of the most important lessons in the entire project.

If the **Repository is the heart of the database**, then the **Service is the brain of the application**.

This is where the application makes decisions.

---

# Goal

By the end of this lesson you'll build:

```text
app/
└── services/
      └── auth_service.py
```

and understand:

* Business Logic
* Dependency Injection
* Registration Flow
* Login Flow
* Password Hashing
* JWT Creation
* Domain Exceptions
* Why Services should NOT know HTTP
* Why Services should NOT know SQL

---

# What is a Service?

Think about registering a user.

Should the repository decide:

* Is the email already taken?
* Should the password be hashed?
* Should JWT be generated?

No.

Those aren't database operations.

They're business rules.

That's exactly what the Service layer is for.

---

# The Complete Flow

```text
Frontend

↓

POST /register

↓

Route

↓

AuthService

↓

UserRepository

↓

PostgreSQL
```

Notice:

The Service sits between the API and the database.

---

# Responsibilities

The AuthService should know how authentication works.

It should:

✅ Check duplicate emails

✅ Hash passwords

✅ Verify passwords

✅ Create JWTs

✅ Return authenticated users

It should NOT:

❌ Execute SQL

❌ Return HTTP responses

❌ Know anything about FastAPI

---

# Create the File

```text
app/
└── services/
      └── auth_service.py
```

---

# Imports

```python
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
```

Notice something.

The Service imports:

* Repository
* Security
* Models
* Schemas

It doesn't import FastAPI.

---

# AuthService Class

```python
class AuthService:

    def __init__(self, db: Session):

        self.repository = UserRepository(db)
```

Let's understand this.

FastAPI injects:

```text
Session
```

↓

Service creates

```text
UserRepository
```

↓

Repository uses Session

Everything shares the same transaction.

---

# Registration Flow

Let's think before coding.

A user registers.

What should happen?

---

## Step 1

Receive

```json
{
    "username":"Navaneeth",
    "email":"nav@gmail.com",
    "password":"MyPassword123"
}
```

---

## Step 2

Check whether the email already exists.

```text
Repository

↓

Find Email
```

If found

↓

Raise an error.

---

## Step 3

Hash the password.

```text
"MyPassword123"

↓

Argon2

↓

$argon2id...
```

---

## Step 4

Create a User model.

Notice.

We don't save the schema.

Schemas represent HTTP.

Models represent the database.

---

## Step 5

Repository saves the user.

---

## Step 6

Return the user.

---

# Implementation

```python
def register_user(
    self,
    data: UserRegister,
) -> User:

    existing_user = self.repository.get_by_email(
        data.email
    )

    if existing_user:
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
```

---

# Understanding Every Line

---

## Find Existing User

```python
existing_user = ...
```

Repository talks to PostgreSQL.

Returns

```python
User
```

or

```python
None
```

---

## Duplicate Check

```python
if existing_user:
```

Business rule.

Repositories shouldn't decide duplicates.

Services do.

---

## Hash Password

```python
hash_password(...)
```

Security belongs to the Service.

Never inside the Repository.

---

## Create User Model

Notice:

```python
User(...)
```

NOT

```python
UserRegister(...)
```

Schemas are temporary.

Models are persistent.

---

## Save

Repository inserts the row.

---

# Login Flow

Now let's design login.

User sends

```json
{
    "email":"nav@gmail.com",
    "password":"secret"
}
```

Flow

```text
Find User

↓

Doesn't Exist?

↓

Error

↓

Verify Password

↓

Wrong Password?

↓

Error

↓

Create JWT

↓

Return Token
```

---

# Implementation

```python
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
```

---

# Why Same Error Message?

Notice:

Wrong email:

```text
Invalid credentials
```

Wrong password:

```text
Invalid credentials
```

Why?

Imagine we returned:

```text
Email doesn't exist
```

An attacker could check which emails are registered.

Returning a generic message prevents user enumeration attacks.

---

# Why Return a Token?

Notice:

```python
return create_access_token(...)
```

The Service does NOT return HTTP.

It simply returns data.

The Route decides how to send it.

---

# Current Architecture

```text
POST /login

↓

Route

↓

AuthService

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

JWT

↓

Route

↓

JSON Response
```

---

# Domain Exceptions

Right now we use:

```python
ValueError
```

This works.

But production applications usually create custom exceptions.

Example:

```python
class EmailAlreadyExistsError(Exception):
    pass
```

and

```python
class InvalidCredentialsError(Exception):
    pass
```

Why?

Because they express intent more clearly and are easier to handle consistently.

We'll introduce custom exceptions in the next lesson.

---

# Why No HTTPException?

Bad:

```python
raise HTTPException(
    status_code=400
)
```

inside the Service.

Why?

The Service shouldn't know:

* FastAPI
* HTTP
* Status Codes

Business logic should be framework-independent.

---

# Visual Flow

Registration

```text
Route

↓

AuthService

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

User
```

---

Login

```text
Route

↓

AuthService

↓

Repository

↓

Database

↓

verify_password()

↓

create_access_token()

↓

JWT
```

---

# Complete Service

```python
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
```

---

# Common Beginner Mistakes

### ❌ SQLAlchemy Queries Inside Services

Wrong.

Use the Repository.

---

### ❌ Hashing Passwords Inside Routes

Wrong.

The Service owns business logic.

---

### ❌ Returning HTTP Responses

Services should return Python objects or raise domain exceptions.

---

### ❌ Creating JWT Inside Routes

Authentication belongs in the Service.

---

### ❌ Returning Password Hashes

Never expose internal security data.

---

# What You Learned Today

You now understand:

* What the Service layer is
* Why business logic belongs there
* How registration works
* How login works
* Email uniqueness checks
* Password hashing
* Password verification
* JWT creation
* Framework-independent services

---

# Mini Challenge

Without looking back, answer these:

1. Why shouldn't the Service execute SQL directly?
2. Why is password hashing performed in the Service instead of the Repository?
3. Why do we return the same error for an invalid email and an invalid password?
4. Why does the Service return a JWT string instead of an HTTP response?
5. What is the difference between a Schema and a Model in the registration flow?
6. Why is the Repository injected into the Service?
7. Why are custom exceptions better than generic `ValueError` in larger projects?

---

# Lesson 20 Preview — Building the Authentication API

So far we have:

* ✅ Schemas
* ✅ Repository
* ✅ Service

Now we'll connect everything to FastAPI.

We'll implement:

* `POST /auth/register`
* `POST /auth/login`
* `GET /users/me`
* Dependency Injection
* HTTP status codes
* Response models
* Exception handling
* Swagger testing

After Lesson 20, you'll have a **fully working authentication system** that you can test from Swagger UI or Postman against your PostgreSQL database. This will be the first complete production-ready module in your Local AI Agent backend.
