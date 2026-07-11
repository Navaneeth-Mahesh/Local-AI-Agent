## Building JWT Authentication in FastAPI

## Goal

By the end of this lesson you'll understand:

* Register Flow
* Login Flow
* OAuth2PasswordBearer
* Access Token Creation
* Token Verification
* Protected Routes
* `get_current_user()`
* Authentication Dependency
* Complete Authentication Architecture

---

# The Big Picture

Let's look at the complete authentication flow.

```text
           Register
              │
              ▼
     Hash Password
              │
              ▼
 Store User in Database


             Login
              │
              ▼
      Verify Password
              │
              ▼
     Create JWT Token
              │
              ▼
 Send Token to Frontend
              │
              ▼
 Store Token
              │
              ▼
 Every API Request
              │
              ▼
 Verify JWT
              │
              ▼
 Get Current User
```

Everything we're going to build fits into this diagram.

---

# Project Structure

By now your project should look similar to this:

```text
app/
│
├── api/
│   ├── routes/
│   │      └── auth.py
│   └── dependencies.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
│
├── database/
│
├── models/
│
├── repositories/
│
├── services/
│
├── schemas/
│
└── main.py
```

Notice something.

Authentication is **not** inside `main.py`.

Professional projects keep authentication isolated.

---

# Step 1 — Authentication Architecture

Before writing code let's understand responsibility.

```text
Frontend

↓

POST /register

↓

API

↓

Service

↓

Repository

↓

Database
```

Login is identical.

```text
Frontend

↓

POST /login

↓

API

↓

Service

↓

Repository

↓

Database
```

Notice:

Routes don't talk directly to the database.

---

# Step 2 — User Registration

What happens when someone registers?

Example:

```text
Username

Navaneeth

Email

nav@gmail.com

Password

MyPassword123
```

Backend flow:

```text
Receive Request

↓

Validate Input

↓

Check Email Exists

↓

Hash Password

↓

Create User

↓

Save User

↓

Return Success
```

Every registration follows these steps.

---

# Step 3 — User Login

Login looks different.

```text
Receive Email

↓

Find User

↓

Verify Password

↓

Generate JWT

↓

Return JWT
```

Notice

We never compare plain passwords.

Only hashes.

---

# Step 4 — OAuth2PasswordBearer

FastAPI provides:

```python
OAuth2PasswordBearer
```

Question:

What does it do?

Many beginners think:

> "It logs users in."

No.

It simply extracts the Bearer Token from the request.

Example request:

```http
Authorization: Bearer eyJhbGc...
```

OAuth2PasswordBearer extracts:

```text
eyJhbGc...
```

That's all.

---

# Create OAuth2 Scheme

Inside

```text
app/api/dependencies.py
```

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
```

---

## What is `tokenUrl`?

Notice:

```python
tokenUrl="/auth/login"
```

It is **documentation**, not functionality.

Swagger UI uses this to know where users obtain a token.

It does **not** create the login endpoint.

---

# Step 5 — Creating Access Tokens

Remember Lesson 13.

JWT contains:

```text
Header

Payload

Signature
```

Now let's implement it.

Inside

```text
core/security.py
```

```python
from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config import settings


def create_access_token(
    user_id: int,
) -> str:

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
```

---

# Understanding Every Line

## Expiration

```python
expire = ...
```

Creates

```text
Current Time

+

30 Minutes
```

---

## Payload

```python
{
    "sub": str(user_id)
}
```

Question:

What is `"sub"`?

JWT defines standard claim names.

`sub`

means

> Subject

In our project,

the subject is

the logged-in user.

---

## Encoding

```python
jwt.encode(...)
```

Signs the JWT

using

```text
SECRET_KEY
```

The frontend receives a signed token.

---

# Step 6 — Verifying Tokens

Now implement:

```python
def verify_access_token(...)
```

Responsibilities:

* Decode JWT
* Verify signature
* Verify expiration
* Return user id

Conceptually:

```text
Incoming Token

↓

Decode

↓

Signature Valid?

↓

Expired?

↓

Extract User ID
```

If any check fails

↓

401 Unauthorized

---

# Step 7 — Current User Dependency

This is where Dependency Injection becomes powerful.

Instead of writing:

```python
verify_token(...)
```

inside every route,

we create:

```python
get_current_user()
```

Flow:

```text
Request

↓

Bearer Token

↓

Verify Token

↓

Load User

↓

Return User Object
```

Every protected route simply receives:

```python
current_user
```

---

# Step 8 — Protected Route

Imagine:

```http
GET /me
```

Without token:

```text
401 Unauthorized
```

With valid token:

```json
{
    "id":1,
    "username":"Navaneeth",
    "email":"nav@gmail.com"
}
```

The route never asks

"Who is this?"

Dependency Injection already answered that.

---

# Step 9 — Complete Request Lifecycle

Imagine:

```text
GET /chat/history
```

FastAPI does:

```text
Receive Request

↓

Extract Bearer Token

↓

Decode JWT

↓

Verify Signature

↓

Check Expiration

↓

Extract User ID

↓

Query Database

↓

Return User

↓

Execute Route
```

The route only runs

after authentication succeeds.

---

# Step 10 — Authentication Dependency

```text
Client

↓

Authorization Header

↓

OAuth2PasswordBearer

↓

verify_access_token()

↓

get_current_user()

↓

Protected Route
```

Notice how every layer has one responsibility.

---

# Why Not Decode JWT in Every Route?

Bad example:

```python
@app.get("/me")
def me():

    decode_jwt()

    ...

@app.get("/chat")
def chat():

    decode_jwt()

    ...

@app.get("/memory")
def memory():

    decode_jwt()

    ...
```

Repeated code.

Instead:

```python
Depends(get_current_user)
```

Authentication becomes reusable.

---

# Complete Architecture

```text
                 Frontend
                      │
                      ▼
              POST /login
                      │
                      ▼
              Auth Service
                      │
                      ▼
           Verify Password Hash
                      │
                      ▼
             Create JWT Token
                      │
                      ▼
               Return JWT
                      │
────────────────────────────────────
                      │
                      ▼
         Authorization: Bearer TOKEN
                      │
                      ▼
          OAuth2PasswordBearer
                      │
                      ▼
        verify_access_token()
                      │
                      ▼
          get_current_user()
                      │
                      ▼
             Protected Endpoint
```

---

# Common Beginner Mistakes

## ❌ Putting email and password inside JWT

JWT should contain minimal information.

Usually

```text
User ID
```

is enough.

---

## ❌ Trusting JWT without verification

Never decode

without verifying

the signature.

---

## ❌ Returning password hashes

Never return

```text
password_hash
```

to the frontend.

---

## ❌ Putting authentication logic inside routes

Keep authentication inside dependencies.

---

## ❌ Skipping expiration

Expired tokens must be rejected.

---

# What We Built

Conceptually,

our authentication system now supports:

* Registration
* Password Hashing
* Login
* JWT Generation
* JWT Verification
* Bearer Authentication
* Protected Routes
* Current User Dependency

This is the same architecture used in many production FastAPI applications.

---

# Mini Challenge

Without looking back, answer these:

1. What is the responsibility of `OAuth2PasswordBearer`?
2. Why do we store the user ID in the JWT instead of the password?
3. What does the `"sub"` claim represent?
4. Why is `get_current_user()` implemented as a dependency?
5. What happens if the JWT signature is invalid?
6. Why should protected routes receive a `current_user` object instead of decoding the JWT themselves?
7. What is the complete login flow from entering a password to receiving a JWT?

If you can answer those, you've understood how JWT authentication works in a real backend.

---

