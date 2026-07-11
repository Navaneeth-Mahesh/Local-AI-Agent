Excellent. This is one of the biggest milestones of Phase 1.

Until now we've built:

* Project structure
* Configuration
* PostgreSQL
* SQLAlchemy
* Models
* Alembic
* Database sessions
* Password hashing

Now we're going to solve one of the most important questions in backend engineering:

> **How does the server remember that a user is logged in?**

This lesson will answer that question.

---

# Phase 1 — Lesson 13: JWT Authentication

## Goal

By the end of this lesson, you'll understand:

* What Authentication is
* Authentication vs Authorization
* Session Authentication
* Token Authentication
* JWT
* JWT Structure
* Header
* Payload
* Signature
* Access Tokens
* Refresh Tokens
* Stateless Authentication
* JWT Lifecycle
* FastAPI JWT implementation
* Protecting API endpoints

---

# First Question

Imagine this.

A user opens your AI Agent.

They log in.

```
Email:
nav@gmail.com

Password:
********
```

Server verifies the password.

Now what?

How does the server know the next request is from the same user?

---

# One Login

```
POST /login
```

Server checks password.

Correct.

User is authenticated.

---

Now the frontend requests:

```
GET /chat/history
```

How does the server know

this request belongs to Navaneeth?

The password isn't sent again.

So what identifies the user?

---

# Two Ways

There are two common methods.

## Method 1

Session Authentication

## Method 2

Token Authentication

We'll use

**Token Authentication**

because it's the standard for APIs.

---

# Session Authentication

Old websites used sessions.

```
Browser

↓

Login

↓

Server creates Session

↓

Stores Session in Memory
```

Example:

```
Session ID

A73JKD92
```

The browser stores:

```
Cookie

↓

A73JKD92
```

Every request sends:

```
Cookie

↓

Server

↓

Looks up Session
```

---

# Problems With Sessions

Imagine:

```
100 Users
```

Easy.

Now imagine

```
10 Million Users
```

The server must remember every session.

That becomes expensive.

Scaling becomes difficult.

---

# Token Authentication

Instead of storing sessions,

the server creates a token.

```
Login

↓

Create Token

↓

Send Token

↓

Frontend Stores Token
```

The server doesn't remember anything.

Every request simply includes the token.

This is called

> **Stateless Authentication**

---

# What Does Stateless Mean?

State means:

Information stored on the server.

Stateless means:

The server stores **no login state**.

Every request contains everything needed.

---

# JWT

JWT stands for

**JSON Web Token**

It is simply a signed string.

Example:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Looks random.

But it has structure.

---

# JWT Structure

Every JWT has three parts.

```
HEADER

.

PAYLOAD

.

SIGNATURE
```

Example:

```
xxxxx.yyyyy.zzzzz
```

Three sections

separated by dots.

---

# Header

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Contains:

* Algorithm
* Token type

---

# Payload

The payload contains data.

Example:

```json
{
    "sub": "42",
    "email": "nav@gmail.com",
    "exp": 1788888888
}
```

Notice:

We don't store the password.

Never.

Usually we store

* User ID
* Email
* Expiration

---

# Signature

The signature prevents tampering.

Imagine someone changes:

```
User ID

42

↓

999
```

The signature becomes invalid.

Server rejects the token.

---

# Visual Diagram

```
Header

↓

Payload

↓

Secret Key

↓

Signature
```

The secret key never leaves the server.

---

# What Is SECRET_KEY?

Remember our `.env`

We'll add

```env
SECRET_KEY=very_long_random_secret_here
```

This key signs every JWT.

If someone doesn't know the key,

they cannot create valid tokens.

---

# Authentication Flow

```
Frontend

↓

POST /login

↓

Verify Password

↓

Create JWT

↓

Send JWT

↓

Frontend Stores JWT
```

---

# Later Requests

```
GET /chat/history

Authorization:

Bearer eyJhbGc...
```

The server reads

```
Bearer Token
```

Verifies it

and knows

```
User = 42
```

---

# Access Token

An access token is short-lived.

Example:

```
15 Minutes
```

or

```
30 Minutes
```

If stolen,

it becomes useless quickly.

---

# Why Not Never Expire?

Imagine

```
Token Valid Forever
```

Attacker steals it.

They now permanently own the account.

Bad.

---

# Refresh Token

Instead,

we use two tokens.

```
Access Token

15 min
```

```
Refresh Token

30 days
```

Access token expires quickly.

Refresh token requests a new access token.

User doesn't need to log in repeatedly.

---

# JWT Lifecycle

```
Login

↓

Access Token

↓

API Calls

↓

Expires

↓

Refresh Token

↓

New Access Token
```

---

# Authentication vs Authorization

These words confuse beginners.

Authentication

↓

Who are you?

Example:

```
Login
```

Authorization

↓

What are you allowed to do?

Example:

```
Admin

↓

Delete User
```

Regular user

↓

Denied

---

# JWT Library

Install:

```bash
pip install python-jose[cryptography]
```

Also install

```bash
pip install python-multipart
```

`python-multipart` is required when working with OAuth2 form-based login in FastAPI.

---

# Why python-jose?

It allows us to:

* Create JWTs
* Verify JWTs
* Check expiration
* Decode payloads

---

# Add to config.py

```python
SECRET_KEY: str

ALGORITHM: str = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

These values come from `.env`.

---

Example

```env
SECRET_KEY=replace_with_a_long_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Create Token Function

Inside

```
security.py
```

We'll later add

```python
def create_access_token():
    ...
```

Responsibilities:

* Accept user ID
* Add expiration
* Sign JWT
* Return token

---

# Verify Token

Another function:

```python
def verify_token():
    ...
```

Responsibilities:

* Decode JWT
* Verify signature
* Verify expiration
* Return user ID

---

# Login Flow

```
Email

↓

Find User

↓

Verify Password

↓

Create JWT

↓

Return JWT
```

---

# Protected Endpoint

Suppose:

```
GET /me
```

Client sends

```
Authorization:

Bearer TOKEN
```

FastAPI

↓

Verify Token

↓

Extract User ID

↓

Load User

↓

Return Profile

---

# What Happens If Token Is Invalid?

```
Token Changed

↓

Signature Invalid

↓

401 Unauthorized
```

---

Expired Token

↓

401 Unauthorized

---

No Token

↓

401 Unauthorized

---

# Where JWT Fits

Our architecture now becomes

```
Frontend

↓

API

↓

Depends(get_current_user)

↓

verify_token()

↓

Repository

↓

Database
```

Notice

The route doesn't manually decode JWT.

A dependency will do it.

---

# Common Beginner Mistakes

### ❌ Putting passwords inside JWT

Never.

---

### ❌ Using a weak SECRET_KEY

Bad

```
password123
```

Good

A long, randomly generated secret (at least 32 bytes).

---

### ❌ Access tokens that never expire

Bad security.

---

### ❌ Trusting JWT without verifying signature

Always verify before using the payload.

---

### ❌ Confusing authentication with authorization

They're different concepts.

---

# JWT vs Sessions

| Sessions              | JWT                   |
| --------------------- | --------------------- |
| Server stores session | Server stores nothing |
| Cookie                | Token                 |
| Harder to scale       | Easy to scale         |
| Traditional websites  | Modern APIs           |

---

# Project Architecture

```
Frontend

↓

Login

↓

FastAPI

↓

Verify Password

↓

JWT

↓

Frontend

↓

Bearer Token

↓

Protected API

↓

Verify JWT

↓

Repository

↓

Database
```

---

# What You Learned Today

You now understand:

* Authentication
* Authorization
* Sessions
* Tokens
* Stateless authentication
* JWT
* JWT structure
* Header
* Payload
* Signature
* SECRET_KEY
* Access Tokens
* Refresh Tokens
* Bearer Authentication
* Protected Routes
* JWT lifecycle

---

# Mini Challenge

Without looking back, answer these:

1. What problem does JWT solve?
2. What does "stateless authentication" mean?
3. What are the three parts of a JWT?
4. Why is the JWT signature important?
5. What's the difference between an Access Token and a Refresh Token?
6. What's the difference between Authentication and Authorization?
7. Why should the `SECRET_KEY` be long and random?
8. Why should access tokens expire?

If you can answer these, you've understood JWT conceptually.

---

