# Implementing the User Module (End-to-End)

This is one of the biggest milestones in the project.

Until now, we've learned **why** things work.

Now we're going to **build** our first complete feature using everything we've learned.

By the end of this lesson, your AI Agent backend will support:

* User Registration
* User Login
* JWT Generation
* Protected Route (`/users/me`)
* Clean Architecture
* Dependency Injection
* PostgreSQL Storage

This is the exact architecture we'll reuse for Conversations, Memory, Documents, Settings, Plugins, and every future module.

---

# What We're Building

```
React Frontend

      │

POST /auth/register

      │

FastAPI Route

      │

Auth Service

      │

User Repository

      │

PostgreSQL
```

---

# Before Writing Code

Let's define responsibilities one last time.

## API Layer

Responsible for

* HTTP
* Status Codes
* Request
* Response

Nothing else.

---

## Service Layer

Responsible for

* Business Rules

Examples

* Hash Password
* Check duplicate email
* Generate JWT

---

## Repository Layer

Responsible for

* SQLAlchemy
* CRUD
* Database Queries

---

## Database

Stores data.

---

# Final Folder Structure

```
backend/

app/

├── api/
│   ├── routes/
│   │      ├── auth.py
│   │      └── users.py
│   │
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
│   └── user.py
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
├── main.py
│
└── exceptions/
```

Notice how every folder has one responsibility.

---

# Step 1 — User Schemas

Create

```
app/schemas/user.py
```

We need three schemas.

---

## Register Request

```python
class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str
```

Incoming JSON.

---

## Login Request

```python
class UserLogin(BaseModel):

    email: EmailStr

    password: str
```

---

## Response Schema

```python
class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr
```

Notice

No password.

No password hash.

Ever.

---

# Step 2 — Repository

Create

```
repositories/user_repository.py
```

Think of repositories like librarians.

You ask:

```
Find user

↓

Repository finds it
```

The repository does not decide *why*.

It simply retrieves data.

---

Methods we need:

```
create()

get_by_email()

get_by_id()
```

---

Example structure

```python
class UserRepository:

    def __init__(self, db):

        self.db = db
```

Notice

No SessionLocal()

Dependency Injection gives us the Session.

---

# create()

Responsibilities

```
Receive User

↓

Insert into Database

↓

Commit

↓

Refresh

↓

Return User
```

---

# get_by_email()

Responsibilities

```
Receive Email

↓

SELECT

↓

Return User

or

None
```

---

# get_by_id()

Responsibilities

```
Receive ID

↓

SELECT

↓

Return User
```

---

# Step 3 — Auth Service

Now comes business logic.

Create

```
services/auth_service.py
```

---

Registration flow

```
UserRegister

↓

Repository

↓

Email Exists?

↓

Yes

↓

Raise Error

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

Notice something.

Hashing belongs here.

Not in Repository.

Because hashing is business logic.

---

# Login Flow

```
Email

↓

Repository

↓

Find User

↓

No User

↓

Raise Error

↓

Verify Password

↓

Wrong Password

↓

Raise Error

↓

Create JWT

↓

Return Token
```

Again

Repository never creates JWT.

---

# Step 4 — API Routes

Now create

```
api/routes/auth.py
```

Routes should be tiny.

Example logic

```
Receive Request

↓

Call Service

↓

Return Response
```

That's it.

---

# Registration Route

```
POST

/auth/register
```

Flow

```
JSON

↓

Schema

↓

Service

↓

Repository

↓

Database

↓

Response Schema

↓

JSON
```

---

Example response

```json
{
    "id":1,
    "username":"Navaneeth",
    "email":"nav@gmail.com"
}
```

---

# Login Route

```
POST

/auth/login
```

Response

```json
{
    "access_token":"eyJhbGc...",

    "token_type":"bearer"
}
```

Very common format.

---

# Why "Bearer"?

Every future request sends

```
Authorization

Bearer eyJhbGc...
```

FastAPI understands this automatically.

---

# Step 5 — get_current_user()

Now we build the most important dependency.

Remember Lesson 14.

```
Token

↓

Decode

↓

Extract User ID

↓

Repository

↓

Load User

↓

Return User
```

Every protected endpoint uses this dependency.

---

Example

```
GET

/users/me
```

No JWT logic inside the route.

Only

```
Depends(get_current_user)
```

---

# What Happens Internally?

Suppose frontend sends

```
Authorization

Bearer TOKEN
```

FastAPI

↓

OAuth2PasswordBearer

↓

verify_access_token()

↓

Extract User ID

↓

Repository.get_by_id()

↓

Return User

↓

Route Executes

---

# Request Lifecycle

Let's trace the complete request.

```
POST /login
```

↓

Route

↓

AuthService.login()

↓

Repository.get_by_email()

↓

Database

↓

Repository returns User

↓

verify_password()

↓

create_access_token()

↓

Route returns JWT

---

Now

```
GET /users/me
```

↓

Bearer Token

↓

Dependency

↓

Verify JWT

↓

Repository

↓

User

↓

Response

---

# Error Handling

Suppose email already exists.

Repository returns

```
User
```

Service raises

```
EmailAlreadyExistsError
```

Route converts to

```
409 Conflict
```

Notice

Repositories never raise HTTP errors.

Only API knows HTTP.

---

# HTTP Status Codes

Successful Registration

```
201 Created
```

Successful Login

```
200 OK
```

Invalid Password

```
401 Unauthorized
```

Duplicate Email

```
409 Conflict
```

Missing Token

```
401 Unauthorized
```

---

# Swagger Testing

After running

```
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

Test order

---

## Register

```
POST

/auth/register
```

Create a user.

---

## Login

```
POST

/auth/login
```

Receive JWT.

---

## Authorize

Click

```
Authorize
```

Paste

```
Bearer TOKEN
```

---

## Test

```
GET

/users/me
```

Should return

```json
{
  "id":1,
  "username":"Navaneeth",
  "email":"nav@gmail.com"
}
```

Congratulations.

Your authentication system works.

---

# Complete Architecture

```
                React

                  │

          POST /register

                  │

               FastAPI

                  │

             Auth Route

                  │

            Auth Service

                  │

          User Repository

                  │

             PostgreSQL

────────────────────────────

             POST /login

                  │

          Verify Password

                  │

            Create JWT

                  │

          Return JWT

────────────────────────────

      Authorization Header

                  │

        get_current_user()

                  │

          Protected Route
```

---

# Why This Architecture Matters

Later, we'll build:

* Conversations
* Messages
* Memory
* File Indexing
* Permissions
* Tool Registry
* Plugin System

Every module follows the exact same structure.

You won't need to invent a new architecture each time.

---

# Common Beginner Mistakes

### ❌ Putting database code inside routes

Routes become large and hard to test.

---

### ❌ Hashing passwords in repositories

Repositories should only interact with the database.

---

### ❌ Returning ORM models directly

Always return Pydantic response schemas.

---

### ❌ Decoding JWT inside every route

Use `get_current_user()` once and inject the authenticated user.

---

### ❌ Mixing HTTP logic with business logic

Services should raise domain errors. Routes decide the HTTP response.

---

# What We Built

You now have the blueprint for a production-style authentication module:

* Schemas for request and response validation
* Repository for database access
* Service for business logic
* API routes for HTTP handling
* JWT authentication
* Protected endpoints
* Dependency Injection
* Clean separation of responsibilities

This is a major milestone—it's the foundation for every other feature in your Local AI Agent.

---

# Mini Challenge

Without looking back, answer these:

1. Why do we separate the API, Service, and Repository layers?
2. Why does password hashing belong in the Service layer?
3. Why shouldn't the Repository return HTTP responses?
4. What is the responsibility of `get_current_user()`?
5. Why do we use response schemas instead of returning ORM models?
6. Which HTTP status code should registration return?
7. What happens from the moment a user clicks "Login" until they successfully access `/users/me`?

---

