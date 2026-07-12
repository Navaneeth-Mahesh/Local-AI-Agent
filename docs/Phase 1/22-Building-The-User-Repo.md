# Building the User Repository (SQLAlchemy 2.0)

---

# Learning Objectives

By the end of this lesson, you will understand:

- What a Repository is
- Why we use the Repository Pattern
- The responsibilities of a Repository
- SQLAlchemy 2.0 querying using `select()`
- The difference between `select()` and the legacy `query()`
- How to read data from PostgreSQL
- How to insert data into PostgreSQL
- What transactions are
- Why `commit()` is required
- Why `refresh()` is required
- Why repositories should never contain business logic

---

# Where We Are in the Project

So far, our application has looked like this:

```text
React Frontend
        │
        ▼
FastAPI API
```

Our API could receive requests, but it had no way to interact with the database.

After today's lesson, the architecture becomes:

```text
React Frontend
        │
        ▼
FastAPI API
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
PostgreSQL Database
```

Today we are building the **Repository Layer**.

This is the first time our backend communicates directly with PostgreSQL.

---

# Understanding the Repository Pattern

## What is a Repository?

A Repository is a class responsible for interacting with the database.

Instead of allowing every part of the application to write SQL queries, we create one dedicated layer that handles all database operations.

The rest of the application simply asks the repository for data.

---

## Why Do We Need a Repository?

Imagine your authentication service needs to find a user.

Without a repository:

```text
Auth Service

↓

SQL Query

↓

Database
```

Now every service in your application must know SQL.

As the project grows, SQL becomes scattered throughout the codebase.

Instead, we introduce a Repository.

```text
Auth Service

↓

User Repository

↓

PostgreSQL
```

Now only one layer understands how to communicate with the database.

This keeps the rest of the application clean and maintainable.

---

# Real-World Analogy

Think about ordering food in a restaurant.

```
Customer

↓

Waiter

↓

Kitchen
```

The customer never walks into the kitchen.

Instead, the waiter communicates with the kitchen on the customer's behalf.

Our application follows the same idea.

```
API

↓

Service

↓

Repository

↓

Database
```

The Service never communicates directly with PostgreSQL.

The Repository acts as the bridge.

---

# Responsibilities of a Repository

A Repository has one responsibility:

**Perform database operations.**

Typical responsibilities include:

- Creating records
- Reading records
- Updating records
- Deleting records
- Listing records

Examples:

```
Create User

Find User

Update User

Delete User

List Users
```

---

## What Does NOT Belong in a Repository?

A Repository should never contain business logic.

The following responsibilities belong elsewhere:

- Hashing passwords
- Generating JWT tokens
- Sending emails
- Checking permissions
- Returning HTTP responses
- Validating business rules

The Repository should only retrieve and store data.

---

# Project Structure

Create the following file:

```text
app/
└── repositories/
    └── user_repository.py
```

This repository will contain all database operations related to the `User` model.

---

# Required Imports

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
```

---

# Understanding the Imports

### `select`

Used to build SQL queries using SQLAlchemy's modern API.

---

### `Session`

Represents an active database session.

All database operations are executed through the session.

---

### `User`

Our SQLAlchemy model representing the `users` table.

---

# Why Use `select()` Instead of `query()`?

Many tutorials still use:

```python
db.query(User)
```

This is the older SQLAlchemy API.

SQLAlchemy 2.0 recommends using:

```python
select(User)
```

Throughout this project, we'll consistently use the modern SQLAlchemy 2.0 style.

---

# Creating the Repository Class

```python
class UserRepository:

    def __init__(self, db: Session):
        self.db = db
```

---

# Understanding the Constructor

The Repository requires access to the database session.

Notice that we are **not** creating a new session.

```python
SessionLocal()
```

should never appear inside a repository.

Instead, the session is provided through Dependency Injection.

This keeps session management centralized and prevents unnecessary database connections.

---

# Method 1 — Find a User by Email

## Problem

Given an email address:

```text
abc@gmail.com
```

We want to retrieve:

```
User
```

or

```
None
```

if no matching user exists.

---

## SQL Equivalent

```sql
SELECT *
FROM users
WHERE email = ?
LIMIT 1;
```

---

## SQLAlchemy Implementation

```python
def get_by_email(
    self,
    email: str,
) -> User | None:

    statement = (
        select(User)
        .where(User.email == email)
    )

    return self.db.scalar(statement)
```

---

# Understanding Every Line

## Step 1 — Build the Query

```python
statement = select(User)
```

Equivalent SQL:

```sql
SELECT * FROM users
```

---

## Step 2 — Add a Filter

```python
.where(User.email == email)
```

Equivalent SQL:

```sql
WHERE email = ?
```

---

## Step 3 — Execute the Query

```python
self.db.scalar(statement)
```

This sends the query to PostgreSQL.

If a matching row exists:

```
User
```

is returned.

Otherwise:

```
None
```

is returned.

---

# Why Use `scalar()`?

Each email address should be unique.

Therefore we expect either:

```
One User
```

or

```
No User
```

We do not need a list of users.

`scalar()` returns a single model instance or `None`, making it ideal for this use case.

---

# Method 2 — Find a User by ID

The implementation is nearly identical.

```python
def get_by_id(
    self,
    user_id: int,
) -> User | None:

    statement = (
        select(User)
        .where(User.id == user_id)
    )

    return self.db.scalar(statement)
```

Notice how the same query pattern can be reused with different filters.

---

# Method 3 — Create a User

Unlike the previous methods, this operation writes data to the database.

The process looks like this:

```text
User Object

↓

Session

↓

add()

↓

commit()

↓

refresh()

↓

Return User
```

---

## Implementation

```python
def create(
    self,
    user: User,
) -> User:

    self.db.add(user)

    self.db.commit()

    self.db.refresh(user)

    return user
```

---

# Understanding Every Line

## `add()`

```python
self.db.add(user)
```

Adds the object to SQLAlchemy's session.

At this point, **nothing has been written to PostgreSQL**.

---

## `commit()`

```python
self.db.commit()
```

Writes all pending changes to the database.

Without calling `commit()`, the inserted row will not be permanently saved.

---

## `refresh()`

```python
self.db.refresh(user)
```

Reloads the object from PostgreSQL.

This ensures the Python object contains the latest values generated by the database.

---

# Why is `refresh()` Important?

Before insertion:

```text
id = None
```

After PostgreSQL inserts the row:

```text
id = 1
```

However, your Python object may still contain:

```text
id = None
```

Calling:

```python
refresh(user)
```

synchronizes the object with the database so it now contains:

```text
id = 1
```

Without `refresh()`, you might return incomplete data to the client.

---

# Understanding Transactions

Creating a user follows this lifecycle:

```text
Create User Object

↓

Track Object

↓

Begin Transaction

↓

INSERT INTO users

↓

COMMIT

↓

Reload Object

↓

Return User
```

A transaction ensures database changes are applied safely and consistently.

---

# Should the Repository Call `commit()`?

This depends on the application's architecture.

### Small and Medium Projects

It's perfectly acceptable for repositories to call:

```python
commit()
```

This keeps the code simple and easy to understand.

---

### Large Enterprise Applications

Many enterprise applications use a **Unit of Work** pattern.

In that architecture:

- The Repository performs database operations.
- The Service controls when transactions are committed.

We'll use the simpler approach for now and refactor later when we study the Unit of Work pattern.

---

# Complete Repository

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .where(User.email == email)
        )
        return self.db.scalar(statement)

    def get_by_id(self, user_id: int) -> User | None:
        statement = (
            select(User)
            .where(User.id == user_id)
        )
        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
```

---

# Visual Request Flow

### Finding a User

```text
API Request

↓

Auth Service

↓

User Repository

↓

SELECT Query

↓

PostgreSQL

↓

User Object

↓

Service

↓

API Response
```

---

### Creating a User

```text
API Request

↓

Auth Service

↓

User Repository

↓

INSERT Query

↓

COMMIT

↓

PostgreSQL

↓

Saved User

↓

Service

↓

API Response
```

---

# Common Beginner Mistakes

### ❌ Hashing passwords inside the Repository

Password hashing belongs in the **Service Layer**.

---

### ❌ Generating JWT tokens

Authentication belongs in the **Service Layer**.

---

### ❌ Creating `SessionLocal()` inside the Repository

The session should always come from Dependency Injection.

---

### ❌ Returning HTTP responses

Repositories should not know anything about HTTP or FastAPI.

---

### ❌ Mixing business rules with database operations

Avoid code like:

```python
if email_exists:
    raise HTTPException(...)
```

The Repository should simply return data.

The Service decides what that data means.

---

# SQLAlchemy 2.0 Best Practice

Instead of:

```python
db.query(User)
```

Prefer:

```python
statement = (
    select(User)
    .where(...)
)

db.scalar(statement)
```

This is the modern SQLAlchemy 2.0 approach and is the style we'll use throughout this project.

---

# Key Takeaways

After completing this lesson, you should understand:

- The purpose of the Repository Pattern.
- Why database access is isolated from business logic.
- How to build queries using `select()`.
- When to use `scalar()`.
- How `add()`, `commit()`, and `refresh()` work together.
- Why repositories should only perform database operations.
- How the Service Layer communicates with PostgreSQL through the Repository Layer.

---

# What's Next?

In the next lesson, we'll build the **Authentication Service**, where we'll use the `UserRepository` to register users, validate existing accounts, hash passwords securely, and prepare our application for JWT-based authentication.