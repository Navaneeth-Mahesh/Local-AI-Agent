## Repository Pattern, Service Layer & Building the User Module

## Goal

By the end of this lesson, you'll understand:

* Clean Architecture
* Repository Pattern
* Service Layer
* Pydantic Schemas
* API Layer
* Flow of a Request
* Separation of Concerns
* Why professional projects don't put everything in routes

---

# Before We Start

Imagine someone clicks **Register**.

They enter:

```text
Username: Navaneeth

Email: nav@gmail.com

Password: MyPassword123
```

Where should the registration logic go?

Many beginners write:

```python
@app.post("/register")
def register():
    # Validate
    # Query database
    # Hash password
    # Create user
    # Commit
    # Return response
```

This works...

Until your project reaches:

* 50 routes
* 100 models
* 20,000 lines of code

Then it becomes a nightmare.

---

# Professional Architecture

Instead, professionals split responsibilities.

```text
Frontend

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

Database
```

Each layer has exactly one responsibility.

---

# The Four Layers

## 1. API Layer

Responsible for:

* Receiving HTTP requests
* Returning HTTP responses
* Calling Services

Nothing more.

---

## 2. Service Layer

Responsible for:

Business Logic.

Examples:

* Hash password
* Check duplicate email
* Create JWT
* Validate permissions

The Service knows **how the application works**.

---

## 3. Repository Layer

Responsible for:

Talking to the database.

Examples:

```text
Find User

Save User

Delete User

Update User
```

The Repository knows SQLAlchemy.

---

## 4. Database

Stores the data.

Nothing else.

---

# Visual Architecture

```text
Browser

↓

POST /register

↓

Auth API

↓

Auth Service

↓

User Repository

↓

PostgreSQL
```

Notice:

The API never touches SQLAlchemy directly.

---

# Why Split Everything?

Suppose tomorrow you switch from PostgreSQL to MySQL.

Should your API change?

No.

Only the Repository changes.

---

Suppose you replace FastAPI with Django.

Should your password hashing logic change?

No.

It lives in the Service.

---

This separation makes the application easier to maintain.

---

# Project Structure

Our project now grows.

```text
app/

├── api/
│   └── routes/
│       └── auth.py
│
├── repositories/
│   └── user_repository.py
│
├── services/
│   └── auth_service.py
│
├── schemas/
│   └── user.py
│
├── models/
│
└── database/
```

Each folder has a clear purpose.

---

# First: Schemas

Before touching the database,

we define the data coming into and out of our API.

---

## What is a Schema?

A Schema defines the shape of data.

Think of it as a contract.

Example request:

```json
{
    "username":"Navaneeth",
    "email":"nav@gmail.com",
    "password":"MyPassword123"
}
```

FastAPI shouldn't accept random JSON.

Schemas enforce the expected structure.

---

# Create

```text
app/schemas/user.py
```

```python
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str
```

---

# Why EmailStr?

Instead of

```python
email: str
```

we use

```python
EmailStr
```

Now:

```text
hello@gmail.com
```

passes.

But

```text
abc
```

fails validation automatically.

---

# Response Schema

Never return:

```python
password_hash
```

Instead:

```python
class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr
```

Notice:

No password.

Ever.

---

# Repository Layer

Create:

```text
repositories/user_repository.py
```

Responsibilities:

```text
Create User

Find User by Email

Find User by ID

Update User

Delete User
```

Nothing else.

---

Example:

```python
class UserRepository:

    def __init__(self, db):
        self.db = db
```

Remember Lesson 11.

Repository receives the Session.

It never creates it.

---

Example methods:

```text
create()

↓

get_by_email()

↓

get_by_id()

↓

delete()
```

Simple.

Focused.

---

# Service Layer

Now create:

```text
services/auth_service.py
```

Responsibilities:

```text
Register User

↓

Hash Password

↓

Check Duplicate Email

↓

Save User
```

The Service combines business rules.

---

Registration flow:

```text
Schema

↓

Validate

↓

Repository

↓

Email Exists?

↓

No

↓

Hash Password

↓

Repository

↓

Save User

↓

Return User
```

---

# Login Service

Flow:

```text
Email

↓

Repository

↓

Find User

↓

Verify Password

↓

Create JWT

↓

Return Token
```

Notice:

The Service doesn't know HTTP.

It only knows business rules.

---

# API Layer

Finally,

create:

```text
api/routes/auth.py
```

Responsibilities:

```text
Receive Request

↓

Call Service

↓

Return Response
```

That's it.

No SQL.

No password hashing.

No JWT generation.

---

# Request Lifecycle

Let's trace one request.

```text
POST /register
```

↓

FastAPI

↓

Schema validates JSON

↓

Service.register()

↓

Repository.create()

↓

Database

↓

Repository returns User

↓

Service returns User

↓

API returns JSON

````

Every layer has one job.

---

# Error Handling

Suppose email already exists.

Should Repository return:

```text
HTTP 400
````

No.

Repositories don't know HTTP.

Instead:

Repository:

```text
User exists
```

↓

Service:

Raises

```text
EmailAlreadyExists
```

↓

API:

Converts to

```text
HTTP 409 Conflict
```

This keeps responsibilities clean.

---

# Why Not Put Everything in Services?

Because Services shouldn't know SQLAlchemy details.

Imagine:

```python
session.query(...)
```

inside Services.

Now business logic is mixed with database code.

Harder to test.

Harder to maintain.

---

# Complete Architecture

```text
Frontend

↓

HTTP Request

↓

API Route

↓

Schema Validation

↓

Service

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

↓

Repository

↓

Service

↓

Response Schema

↓

JSON Response
```

This is the architecture we'll use for every feature:

* Chat
* Memory
* Documents
* Permissions
* Plugins
* Settings

---

# Dependency Injection

Notice how dependencies flow.

```text
FastAPI

↓

Depends(get_db)

↓

Session

↓

Repository

↓

Service

↓

Route
```

Nothing creates dependencies manually.

Everything is injected.

---

# Common Beginner Mistakes

### ❌ SQLAlchemy inside Routes

```python
@app.post("/register")

db.query(...)
```

Routes become huge.

---

### ❌ Password Hashing inside Repository

Repositories shouldn't know security.

---

### ❌ JWT inside Repository

Authentication belongs to Services.

---

### ❌ Returning ORM Models Directly

Always return Response Schemas.

---

### ❌ One File for Everything

Avoid:

```text
main.py

↓

3000 lines
```

Organize by responsibility.

---

# What We've Built

Our authentication feature now has a clear architecture:

```text
Register

↓

UserRegister Schema

↓

Auth Service

↓

User Repository

↓

Database

↓

UserResponse Schema

↓

Frontend
```

The same pattern will be reused throughout the AI Agent.

---

# Mini Challenge

Answer these without looking back:

1. What is the responsibility of the **API Layer**?
2. Why should the **Repository** not hash passwords?
3. Why should the **Service** not contain SQLAlchemy queries?
4. What is the purpose of a **Schema**?
5. Why do we return `UserResponse` instead of the `User` model?
6. Why does the Repository receive a Session instead of creating one?
7. If tomorrow you switch databases, which layer changes the most?

If you can answer these confidently, you've understood one of the most valuable architectural patterns in backend engineering.

---

