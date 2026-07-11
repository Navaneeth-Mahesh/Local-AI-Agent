## Building the User Repository (SQLAlchemy 2.0)

This lesson is where your backend talks to PostgreSQL for the first time through a proper repository.

Until now:

```text
Frontend
    ↓
FastAPI
```

After today:

```text
Frontend
    ↓
FastAPI
    ↓
Repository
    ↓
PostgreSQL
```

This is your first real database layer.

---

# Goal

By the end of this lesson you'll understand:

* What a Repository actually is
* Why we use the Repository Pattern
* SQLAlchemy 2.0 querying
* `select()` vs `query()`
* Creating records
* Reading records
* Transactions
* `commit()`
* `refresh()`
* Why repositories should NOT contain business logic

---

# What is a Repository?

Imagine your Service needs a user.

Should it know SQL?

No.

Instead it asks someone else.

```text
Auth Service

↓

User Repository

↓

Database
```

The Repository is the only layer responsible for talking to PostgreSQL.

---

# Real World Analogy

Imagine a restaurant.

Customer:

> I want Pizza.

Waiter:

Takes order.

Kitchen:

Makes pizza.

The customer never walks into the kitchen.

Likewise,

```text
API

↓

Service

↓

Repository

↓

Database
```

The Service never writes SQL.

---

# Responsibilities

A repository should only do database operations.

Good:

```text
Create User

Find User

Update User

Delete User

List Users
```

Bad:

```text
Hash Password

Generate JWT

Send Email

Check Permissions
```

Those belong elsewhere.

---

# Project Structure

Create:

```text
app/

repositories/

    user_repository.py
```

---

# Imports

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
```

---

## Why `select()`?

Older tutorials use:

```python
db.query(User)
```

This is the legacy style.

SQLAlchemy 2.0 recommends:

```python
select(User)
```

We'll use the modern API throughout this project.

---

# Repository Class

```python
class UserRepository:

    def __init__(self, db: Session):
        self.db = db
```

Remember Lesson 11.

We never create:

```python
SessionLocal()
```

Dependency Injection already gave us the Session.

---

# Method 1 — Get User by Email

Let's think first.

Input:

```text
Email
```

Output:

```text
User

or

None
```

---

### SQL Equivalent

```sql
SELECT *
FROM users
WHERE email = ?
LIMIT 1;
```

---

### SQLAlchemy

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

## Let's Understand Every Line

### Step 1

```python
statement = select(User)
```

Means:

```sql
SELECT * FROM users
```

---

### Step 2

```python
.where(User.email == email)
```

Adds

```sql
WHERE email = ?
```

---

### Step 3

```python
self.db.scalar(statement)
```

This executes the query.

Returns:

```python
User
```

or

```python
None
```

---

# Why `scalar()`?

Suppose only one user should exist.

```text
Email

↓

One User
```

We don't need:

```python
list[User]
```

We only need

```python
User | None
```

---

# Method 2 — Get User by ID

Very similar.

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

Notice how reusable `select()` is.

---

# Method 3 — Create User

This one is different.

We're inserting data.

Flow:

```text
Receive User

↓

Add

↓

Commit

↓

Refresh

↓

Return User
```

Implementation:

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

Tells SQLAlchemy:

> "Track this object."

Nothing has been written yet.

---

## `commit()`

```python
self.db.commit()
```

Actually saves the row.

Without commit:

```text
Database unchanged.
```

---

## `refresh()`

This confuses almost everyone.

Imagine:

Before insert:

```text
id = None
```

Database inserts:

```text
id = 1
```

Your Python object still says:

```text
None
```

Until:

```python
refresh(user)
```

Now:

```text
id = 1
```

The object is synchronized with PostgreSQL.

---

# Why Refresh Matters

Suppose we immediately return:

```json
{
    "id": null
}
```

Bad.

Refresh reloads the latest values.

---

# Transaction Lifecycle

Creating a user looks like:

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

# Should Repository Commit?

This is an advanced topic.

For small projects:

```text
Repository

↓

Commit
```

is acceptable.

For large enterprise systems,

the Service or Unit of Work often controls commits.

We'll keep commits inside the repository for now to keep the project easier to understand.

Later, when we discuss the **Unit of Work Pattern**, we'll refactor this.

---

# Complete Repository

```python
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.email == email)
        )

        return self.db.scalar(statement)

    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.id == user_id)
        )

        return self.db.scalar(statement)

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

# Visual Flow

```text
Auth Service

↓

Repository.get_by_email()

↓

SELECT

↓

PostgreSQL

↓

User

↓

Service
```

Registration:

```text
Auth Service

↓

Repository.create()

↓

INSERT

↓

COMMIT

↓

RETURN USER
```

---

# Common Beginner Mistakes

### ❌ Hashing Passwords Here

Wrong.

Repositories shouldn't know security.

---

### ❌ Creating JWT Here

Wrong.

Authentication belongs to the Service layer.

---

### ❌ Using `SessionLocal()` Inside Repository

Wrong.

Dependency Injection already provides a Session.

---

### ❌ Returning HTTP Responses

Repositories should never know about HTTP.

---

### ❌ Mixing Business Logic

Avoid code like:

```python
if email_exists:
    raise HTTPException(...)
```

The repository should simply return the data.

The Service decides what it means.

---

# Modern SQLAlchemy Pattern

Instead of:

```python
db.query(User)
```

We'll consistently use:

```python
statement = (
    select(User)
    .where(...)
)

db.scalar(statement)
```

This is the recommended SQLAlchemy 2.0 style and is what you'll see in modern production code.

---

# What You Learned Today

You now understand:

* The Repository Pattern
* SQLAlchemy 2.0 `select()`
* `scalar()`
* `add()`
* `commit()`
* `refresh()`
* Repository responsibilities
* Why repositories avoid business logic
* How Services communicate with the database

---

