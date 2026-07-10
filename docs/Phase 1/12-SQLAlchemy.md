## SQLAlchemy ORM & Database Connection

## Goal

By the end of this lesson, you'll understand:

* What an ORM is
* Why ORMs exist
* SQLAlchemy Architecture
* Engine
* Connection
* Session
* Declarative Base
* Models
* Metadata
* Creating a reusable database layer
* Connecting FastAPI to PostgreSQL

---

# Before We Start

Suppose you want to create a user.

Without an ORM, you'd write:

```sql
INSERT INTO users (username, email)
VALUES ('Navaneeth', 'nav@gmail.com');
```

Now imagine your project grows to:

* Users
* Messages
* Conversations
* Memories
* Plugins
* Permissions
* Documents

You'll end up writing hundreds of SQL queries.

---

# What is an ORM?

ORM stands for:

> **Object Relational Mapper**

Let's understand each word.

---

## Object

Python works with objects.

```python
user = User(
    username="Navaneeth",
    email="nav@gmail.com"
)
```

This is a Python object.

---

## Relational

PostgreSQL stores data in tables.

```text
Users

-------------------------
id | username | email
-------------------------
1  | Navaneeth| nav@gmail.com
```

---

## Mapper

SQLAlchemy maps:

```text
Python Object

↓

Database Row
```

Instead of writing SQL manually, you work with Python objects.

---

# Visual Representation

Without ORM

```text
Python

↓

Raw SQL

↓

PostgreSQL
```

With ORM

```text
Python

↓

SQLAlchemy

↓

SQL

↓

PostgreSQL
```

SQLAlchemy translates your Python code into SQL.

---

# Does SQLAlchemy Replace SQL?

No.

This is a very common misconception.

SQLAlchemy **generates SQL**.

Example:

You write:

```python
session.add(user)
```

SQLAlchemy internally generates:

```sql
INSERT INTO users (...)
VALUES (...);
```

The database still executes SQL.

---

# Why Use an ORM?

Imagine you want all users.

Raw SQL:

```sql
SELECT *
FROM users;
```

SQLAlchemy:

```python
session.query(User).all()
```

More Pythonic.

Easier to maintain.

---

# SQLAlchemy Architecture

This is the most important diagram today.

```text
FastAPI

↓

Session

↓

Engine

↓

PostgreSQL
```

Let's understand each layer.

---

# Engine

The Engine is the entry point to the database.

Think of it as:

```text
Database Manager
```

Responsibilities:

* Opens connections
* Closes connections
* Manages connection pool
* Sends SQL

Without an Engine,

nothing can talk to PostgreSQL.

---

# Connection

The Engine creates a connection.

```text
FastAPI

↓

Engine

↓

Connection

↓

Database
```

A connection is like opening a phone call.

When you're done,

the call ends.

---

# Session

Instead of working directly with connections,

applications use a Session.

Think of the Session as:

> A workspace for database operations.

Inside one session you can:

* Create users
* Update messages
* Delete conversations

Then save everything together.

---

# Real Life Analogy

Imagine Google Docs.

You edit the document.

Nothing is permanently saved until you press Save.

The Session works similarly.

You make changes.

Then:

```python
session.commit()
```

Everything is saved.

---

# Declarative Base

Instead of manually creating tables,

we create Python classes.

Example:

```python
class User(Base):
    ...
```

SQLAlchemy understands:

> This class represents a database table.

---

# Model

Every table becomes a Python class.

Example:

Database

```text
Users Table
```

↓

Python

```python
class User(Base):
```

Another table

```text
Messages
```

↓

Python

```python
class Message(Base):
```

Models represent tables.

---

# Metadata

SQLAlchemy keeps track of every model.

```text
User

Conversation

Message

Memory
```

All are registered inside Metadata.

Later,

Metadata can create all tables automatically.

---

# Installing SQLAlchemy

Inside your virtual environment:

```bash
pip install sqlalchemy psycopg2-binary
```

Then update:

```bash
pip freeze > requirements.txt
```

---

## Why `psycopg2-binary`?

SQLAlchemy is an ORM.

It doesn't directly communicate with PostgreSQL.

It needs a database driver.

```text
FastAPI

↓

SQLAlchemy

↓

psycopg2

↓

PostgreSQL
```

`psycopg2-binary` is the driver.

---

# Project Structure

We'll now use the `database/` folder we created earlier.

```text
backend/

app/

database/
    ├── base.py
    ├── session.py
    └── __init__.py
```

---

# Step 1 — Create `session.py`

**Location**

```text
app/database/session.py
```

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
```

---

# Understanding Every Line

## Import

```python
from sqlalchemy import create_engine
```

Creates the Engine.

---

```python
from sqlalchemy.orm import sessionmaker
```

Creates Sessions.

---

## Engine

```python
engine = create_engine(...)
```

This creates the application's connection to PostgreSQL.

---

## `DATABASE_URL`

```python
settings.DATABASE_URL
```

Comes from:

```text
.env
```

Example:

```text
postgresql://postgres:password@localhost:5432/ai_agent
```

---

## `echo=settings.DEBUG`

If `DEBUG=True`

Every SQL query appears in the terminal.

Example:

```sql
SELECT *
FROM users;
```

Very useful while learning.

In production,

`DEBUG=False`.

---

# SessionLocal

```python
SessionLocal = sessionmaker(...)
```

This creates a factory.

Think of it like this:

```text
Session Factory

↓

New Session

↓

New Session

↓

New Session
```

Every request gets its own Session.

---

## `autocommit=False`

Changes are **not** saved automatically.

You decide when to save.

```python
session.commit()
```

This prevents accidental writes.

---

## `autoflush=False`

SQLAlchemy won't automatically push pending changes to the database before every query. You'll explicitly `commit()` (or `flush()` when needed), making database interactions more predictable while you're learning.

---

# Step 2 — Create `base.py`

**Location**

```text
app/database/base.py
```

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

---

# Why This Exists

Every model will inherit from `Base`.

Example:

```python
class User(Base):
    ...
```

```python
class Conversation(Base):
    ...
```

```python
class Message(Base):
    ...
```

This tells SQLAlchemy:

> "These are database models."

---

# Updated Project Structure

```text
backend/
│
├── app/
│   │
│   ├── api/
│   ├── core/
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── __init__.py
│   │
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
└── .env
```

---

# What Happens When FastAPI Starts?

```text
FastAPI Starts

↓

config.py

↓

Reads DATABASE_URL

↓

session.py

↓

Creates Engine

↓

Session Factory Ready

↓

Application Starts
```

Notice:

No connection is opened yet.

The Engine is simply ready.

Connections are opened only when needed.

---

# Why We Haven't Created Tables Yet

Right now, we've built the **database infrastructure**, not the database schema.

We still need to define:

* User
* Conversation
* Message
* Memory

Those Python models become database tables.

We'll build them in the next lesson.

---

# What You Learned Today

You now understand:

* What an ORM is
* Why ORMs exist
* SQLAlchemy's role
* Why SQLAlchemy does not replace SQL
* Engine
* Connection
* Session
* Session Factory
* Declarative Base
* Models
* Metadata
* How to connect FastAPI to PostgreSQL
* Why the database layer is separated into its own package

---

# Mini Challenge

Before moving on, make sure you can answer:

1. What problem does an ORM solve?
2. Does SQLAlchemy replace SQL?
3. What is the responsibility of the **Engine**?
4. What is a **Session**, and why don't we use connections directly?
5. Why do we set `autocommit=False`?
6. Why does every model inherit from `Base`?
7. Why do we keep the Engine and Session creation in `session.py` instead of `main.py`?

If you can explain these concepts in your own words, you're ready for the next step.

---


