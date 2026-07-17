# Building User Schemas

---

# Learning Objectives

By the end of this lesson, you will understand:

* What a schema is
* Why we create schemas before writing business logic
* The difference between a Schema and a Database Model
* Why different API operations require different schemas
* How Pydantic validates incoming data
* How response schemas protect sensitive information
* How schemas fit into our backend architecture

---

# What Are We Building?

Today we'll write our **first production code**.

We'll create the following file:

```text
app/
└── schemas/
    └── user.py
```

Inside this file we'll build all the schemas required for authentication.

```text
UserRegister

UserLogin

UserResponse

Token

TokenPayload
```

These schemas define how the frontend and backend communicate.

---

# Why Do We Start with Schemas?

Before writing database code or business logic, we first decide **what data our API should accept and return**.

Professional backend development often follows this order:

```text
Design the API

↓

Create Schemas

↓

Write Business Logic

↓

Create Database Models

↓

Build API Routes
```

This is called an **API-First Approach**.

The frontend developer needs to know:

* What data should be sent?
* Which fields are required?
* What data will be returned?

Schemas answer these questions.

They act as a contract between the frontend and backend.

---

# What is a Schema?

A **Schema** defines the structure of data entering or leaving our application.

Think of it as a blueprint.

A schema tells FastAPI:

* Which fields are required
* Which data types are allowed
* How to validate the data
* What the response should look like

Schemas **do not store data**.

They only describe data.

---

# Schema vs Database Model

One of the biggest beginner mistakes is thinking a Schema and a Database Model are the same thing.

They are not.

---

## Database Model

A Database Model represents a table inside PostgreSQL.

Example:

```text
users

├── id
├── username
├── email
├── password_hash
├── created_at
└── updated_at
```

The database stores **everything**.

Including fields users should never see.

---

## Pydantic Schema

A Schema represents data sent through the API.

Example request:

```json
{
    "username": "Navaneeth",
    "email": "nav@gmail.com",
    "password": "MyPassword123"
}
```

Notice that it does **not** contain:

* id
* created_at
* updated_at
* password_hash

Those values are created by the backend.

---

# Where Does a Schema Fit?

Every request travels through multiple layers.

```text
Frontend

↓

Schema

↓

Service

↓

Repository

↓

Database Model

↓

PostgreSQL
```

When the response comes back:

```text
PostgreSQL

↓

Database Model

↓

Service

↓

Response Schema

↓

Frontend
```

Schemas are the bridge between the frontend and backend.

---

# User Registration Example

Suppose a user clicks **Register**.

The frontend sends:

```json
{
    "username": "Navaneeth",
    "email": "nav@gmail.com",
    "password": "MyPassword123"
}
```

The backend automatically creates:

* User ID
* Password Hash
* Created Time
* Updated Time

The user never sends those values.

---

# Registration Response

After successful registration, the backend returns:

```json
{
    "id": 1,
    "username": "Navaneeth",
    "email": "nav@gmail.com"
}
```

Notice what is missing.

We never return:

* Password
* Password Hash

Sensitive information should never be exposed through the API.

---

# Why Create Multiple Schemas?

Many beginners create one schema like this:

```python
UserSchema
```

and use it for everything.

This quickly becomes confusing.

Different API operations require different data.

Registration needs:

```text
Username

Email

Password
```

Login needs:

```text
Email

Password
```

The response contains:

```text
ID

Username

Email
```

Instead of one large schema, we create several small schemas.

Each schema has one responsibility.

---

# Schemas We'll Build

Our authentication module requires five schemas.

```text
UserRegister

↓

UserLogin

↓

UserResponse

↓

Token

↓

TokenPayload
```

Let's build them one by one.

---

# Project Structure

Create:

```text
app/

└── schemas/

    └── user.py
```

---

# Step 1 — Import Pydantic

```python
from pydantic import BaseModel, ConfigDict, EmailStr
```

Let's understand these imports.

---

## BaseModel

Every Pydantic schema inherits from `BaseModel`.

```python
class UserRegister(BaseModel):
```

`BaseModel` provides:

* Data validation
* Type checking
* JSON serialization
* Error handling
* Automatic Swagger documentation

Without it, FastAPI wouldn't recognize the class as a schema.

---

## EmailStr

Instead of:

```python
email: str
```

we use:

```python
email: EmailStr
```

Now:

✅

```text
hello@gmail.com
```

passes validation.

But:

❌

```text
abc
```

fails automatically.

No extra validation code is needed.

---

# Step 2 — User Registration Schema

```python
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
```

Used by:

```http
POST /auth/register
```

Expected request:

```json
{
    "username": "Navaneeth",
    "email": "nav@gmail.com",
    "password": "MyPassword123"
}
```

---

# Step 3 — User Login Schema

```python
class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

Used by:

```http
POST /auth/login
```

Notice that login doesn't require a username.

Only:

* Email
* Password

---

# Step 4 — User Response Schema

```python
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )
```

This schema defines what the backend sends back to the frontend.

Example:

```json
{
    "id": 1,
    "username": "Navaneeth",
    "email": "nav@gmail.com"
}
```

---

# Understanding `from_attributes=True`

This is an important feature in **Pydantic v2**.

SQLAlchemy returns Python objects.

Example:

```python
user = User(...)
```

The object looks like:

```python
user.id
user.username
user.email
```

However, Pydantic normally expects a dictionary.

```python
{
    "id": 1,
    "username": "Navaneeth"
}
```

By adding:

```python
from_attributes=True
```

we tell Pydantic:

> "Read values directly from object attributes."

Without it, converting SQLAlchemy models into response schemas would fail.

---

# Step 5 — Token Schema

After a successful login, the backend returns a JWT.

Example response:

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

Schema:

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

---

# Step 6 — Token Payload Schema

Inside every JWT is a payload.

Initially we'll only store the user ID.

Example:

```json
{
    "sub": "1"
}
```

Schema:

```python
class TokenPayload(BaseModel):
    sub: str
```

Later we'll add more JWT claims.

---

# Complete `user.py`

```python
from pydantic import BaseModel, ConfigDict, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
```

---

# Why Aren't We Validating Passwords Yet?

You might notice that:

```python
password: str
```

still accepts:

```text
123
```

This is intentional.

Right now we're building the application's architecture.

In future lessons we'll improve these schemas by adding:

* Minimum length
* Maximum length
* Strong password rules
* Username validation
* Custom validators

Building step by step makes each concept easier to understand.

---

# Where Do These Schemas Fit?

Our registration flow now looks like this:

```text
Frontend

↓

UserRegister Schema

↓

Auth Service

↓

User Repository

↓

User Model

↓

PostgreSQL

↓

UserResponse Schema

↓

Frontend
```

Every request entering the backend passes through a schema.

Every response leaving the backend also passes through a schema.

This ensures our API always sends and receives valid, predictable data.

---

# Key Takeaways

After this lesson, you should understand:

* A Schema defines the structure of API data.
* Schemas are different from Database Models.
* Schemas validate incoming requests and format outgoing responses.
* Different API operations require different schemas.
* `BaseModel` powers validation and serialization.
* `EmailStr` automatically validates email addresses.
* `from_attributes=True` allows Pydantic to read SQLAlchemy objects.
* Response schemas protect sensitive information like passwords.
* Schemas are the communication bridge between the frontend and backend.


