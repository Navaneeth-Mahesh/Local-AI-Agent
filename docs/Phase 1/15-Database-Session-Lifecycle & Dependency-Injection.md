Excellent. This lesson separates developers who **can build CRUD apps** from developers who **understand backend architecture**.

Many FastAPI tutorials teach:

```python
@app.get("/users")
def get_users():
    db = SessionLocal()
    ...
```

It works.

But it's not how production applications are built.

Today you'll understand **why**.

---

# Phase 1 — Lesson 11: Database Session Lifecycle & Dependency Injection

## Goal

By the end of this lesson, you'll understand:

* What a Database Session really is
* Why each request gets its own Session
* Session Lifecycle
* Dependency Injection (DI)
* FastAPI's `Depends()`
* Generator Dependencies (`yield`)
* Why Sessions must always close
* Repository Pattern integration
* Unit of Work concept
* How professional FastAPI projects manage database access

---

# Before We Start

Let's revisit something from Lesson 8.

We created:

```python
engine = create_engine(...)
```

and

```python
SessionLocal = sessionmaker(...)
```

Question:

**Does this mean our application has one Session forever?**

No.

This is one of the biggest misconceptions beginners have.

---

# Engine vs Session

Remember this forever.

```
Engine
```

is

> The database manager.

Usually only **one Engine** exists.

---

```
Session
```

is

> A temporary workspace for one database interaction.

Many Sessions are created.

---

Think like this:

```
One Engine

↓

Session

↓

Closed

↓

Session

↓

Closed

↓

Session

↓

Closed
```

The Engine lives for the application's lifetime.

Sessions live only for a request.

---

# Real World Analogy

Imagine a bank.

```
Bank Building

↓

Customers
```

The bank building doesn't disappear.

Customers enter.

Finish work.

Leave.

---

Engine

↓

Bank Building

Session

↓

Customer

---

# Why Not One Session Forever?

Imagine User A logs in.

Session stores:

```
User A
```

Now User B logs in.

Same Session.

Now imagine:

```
User A modifies data.

↓

User B reads data.

↓

Unexpected behavior.
```

Sessions would interfere with each other.

That would be terrible.

---

Instead:

```
Request 1

↓

Session 1

↓

Closed
```

```
Request 2

↓

Session 2

↓

Closed
```

Every request gets its own Session.

---

# Session Lifecycle

A Session has a beginning and an end.

```
HTTP Request

↓

Create Session

↓

Run Queries

↓

Commit / Rollback

↓

Close Session

↓

Response
```

This happens on **every request**.

---

# Why Closing Matters

Imagine opening files.

```python
open("file.txt")
```

If you never close them,

eventually:

```
Too many open files
```

The same idea applies to database connections.

Leaving Sessions open eventually exhausts available database connections.

Always close them.

---

# Manual Session Management

You could write:

```python
db = SessionLocal()

try:
    users = db.query(User).all()

finally:
    db.close()
```

Works.

But imagine writing this in 80 endpoints.

You'll repeat the same code everywhere.

---

# FastAPI's Solution

FastAPI provides:

```python
Depends()
```

This is called **Dependency Injection (DI)**.

---

# What is Dependency Injection?

Instead of a function creating what it needs,

someone else provides it.

Without DI:

```
Route

↓

Creates Session

↓

Uses Session
```

With DI:

```
Route

↓

Receives Session
```

The route doesn't care how the Session was created.

---

# Everyday Example

Imagine ordering food.

Without DI:

```
Cook rice

Cook curry

Prepare plate

Serve yourself
```

With DI:

Restaurant does everything.

You simply receive the food.

FastAPI works similarly.

---

# Create a Dependency

Create:

```
app/database/dependencies.py
```

```python
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

This is one of the most important functions in the project.

---

# Understanding Every Line

## Create Session

```python
db = SessionLocal()
```

Creates a brand-new Session.

Not Engine.

Not Connection.

A Session.

---

## yield

This is Python's Generator feature.

Instead of:

```python
return db
```

we write:

```python
yield db
```

Why?

Because FastAPI needs to execute code **after** the request finishes.

---

Flow:

```
Create Session

↓

yield

↓

Route Executes

↓

finally

↓

db.close()
```

The Session is guaranteed to close.

---

# Why Not Return?

Suppose we wrote:

```python
return db
```

After returning,

the function is finished.

It cannot execute:

```python
db.close()
```

With `yield`,

FastAPI pauses the function,

runs the route,

then resumes execution,

allowing cleanup.

---

# Using Depends

Example route:

```python
from fastapi import Depends
from sqlalchemy.orm import Session


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    ...
```

Notice something.

We never create:

```python
SessionLocal()
```

FastAPI does it.

---

# What Happens Internally?

```
HTTP Request

↓

Depends(get_db)

↓

Create Session

↓

Inject Session

↓

Route Runs

↓

Route Returns

↓

Close Session
```

Everything happens automatically.

---

# Dependency Injection Benefits

The route becomes much cleaner.

Instead of:

```python
db = SessionLocal()
```

everywhere,

we simply receive:

```python
db
```

Professional code focuses on business logic,

not infrastructure.

---

# Repository Pattern

Remember our architecture.

```
API

↓

Service

↓

Repository

↓

Database
```

The Repository also receives the Session.

Example:

```python
class UserRepository:

    def __init__(self, db: Session):
        self.db = db
```

Notice.

Repository never creates Sessions.

It receives one.

This makes repositories easier to test and reuse.

---

# Why One Session Per Request?

Imagine registration.

```
Create User

↓

Create Settings

↓

Create Default Conversation
```

Should each use different Sessions?

No.

All three operations belong to one logical unit.

Everything should happen inside one Session.

If something fails:

```
Rollback

↓

Nothing Saved
```

Consistency is maintained.

---

# Unit of Work

This idea has a name.

> **Unit of Work**

One Session

↓

One Request

↓

One Transaction

↓

Commit

or

Rollback

Everything succeeds together,

or everything fails together.

---

# Commit vs Rollback

Imagine:

```
Create User

✓
```

```
Create Conversation

✓
```

```
Create Memory

❌
```

Without transactions:

Half the data is saved.

With a single Session:

```
Rollback

↓

Database returns to previous state.
```

Nothing partial remains.

---

# Visual Architecture

```
FastAPI Request

↓

Depends(get_db)

↓

Session

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

↓

Commit

↓

Close Session
```

This is the architecture we'll use throughout the project.

---

# Updated Project Structure

```
app/

database/

├── base.py
├── session.py
├── dependencies.py
└── __init__.py
```

---

# Best Practices

✅ One Engine for the application

✅ One Session per request

✅ Always close Sessions

✅ Never create Sessions inside repositories

✅ Never create Sessions inside services

✅ Use `Depends(get_db)`

✅ Use `yield` for cleanup

---

# Common Beginner Mistakes

### ❌ Creating a Session globally

```python
db = SessionLocal()
```

at import time.

This Session stays alive indefinitely.

---

### ❌ Creating a new Session inside every repository

```
UserRepository()

↓

SessionLocal()
```

Now different repositories use different transactions.

Bad.

---

### ❌ Forgetting to close Sessions

Eventually:

```
Connection Pool Exhausted
```

The application stops serving requests.

---

### ❌ Calling `commit()` everywhere

Repositories shouldn't randomly commit.

We'll discuss proper commit responsibility when we build the Service layer.

---

# What You Learned Today

You now understand:

* Engine vs Session
* Session Lifecycle
* Why Sessions are temporary
* Dependency Injection
* `Depends()`
* Generator dependencies
* `yield`
* Automatic cleanup
* Repository injection
* Unit of Work
* One Session per request

---

# Mini Challenge

Without looking back, answer these:

1. What's the difference between an **Engine** and a **Session**?
2. Why shouldn't a Session live forever?
3. Why does `get_db()` use `yield` instead of `return`?
4. What problem does `Depends(get_db)` solve?
5. Why shouldn't repositories create their own Sessions?
6. What is the **Unit of Work** pattern?
7. Why is closing Sessions important?

If you can answer those confidently, you've understood one of the most important concepts in FastAPI.

---

# Before Lesson 12: A Production Improvement

Everything we've built so far is solid, but there's one architectural improvement I'd make before continuing.

Instead of placing `get_db()` in `database/dependencies.py`, many production projects organize dependencies by purpose:

```
app/
├── api/
│   └── dependencies.py
├── core/
├── database/
│   ├── base.py
│   └── session.py
```

* `database/session.py` remains responsible for creating database sessions.
* `api/dependencies.py` becomes the place where FastAPI dependencies (database sessions, current user, permission checks, etc.) are defined.

This keeps the **database layer framework-agnostic** and the **API layer responsible for FastAPI-specific concerns**. As our project grows to include authentication, authorization, and permissions, this organization scales more naturally.

In **Lesson 12**, we'll move into **Password Security**:

* Why passwords are never stored in plain text
* Hashing vs Encryption
* Salting
* Argon2 vs bcrypt
* Password verification
* Completing the first real implementation inside `security.py`

This is the foundation for building a secure authentication system.
