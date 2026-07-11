SQLAlchemy Models & Relationships

## Goal

By the end of this lesson, you'll understand:

* What a Model is
* What `Mapped[]` is
* What `mapped_column()` is
* How SQLAlchemy creates tables
* `__tablename__`
* Primary Keys
* Foreign Keys
* Relationships
* One-to-Many relationships
* Timestamps
* Best practices for model organization

---

# Before We Write Code

Imagine our AI Agent after six months.

Thousands of users.

Each user has:

* Profile
* Chat History
* AI Memories
* Uploaded Documents
* Settings
* API Keys

How do we represent this in Python?

Instead of writing SQL tables manually...

We create **Python classes**.

---

# What is a Model?

A Model is simply:

> **A Python class that represents a database table.**

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
Messages Table
```

↓

Python

```python
class Message(Base):
```

Every table becomes a class.

---

# Our AI Agent Database

We'll eventually have these models:

```text
User
│
├── Conversation
│      └── Message
│
├── Memory
│
├── Document
│
├── Permission
│
└── Setting
```

Today we'll build the first three.

---

# Project Structure

Inside `models/`:

```text
app/
│
├── models/
│     ├── user.py
│     ├── conversation.py
│     ├── message.py
│     └── __init__.py
```

Each model gets its own file.

As the project grows, this keeps things organized.

---

# SQLAlchemy 2.0 Style

Older SQLAlchemy versions looked like this:

```python
id = Column(Integer, primary_key=True)
```

This still works.

But SQLAlchemy 2.0 introduced a cleaner, type-safe approach.

```python
id: Mapped[int] = mapped_column(primary_key=True)
```

We'll use the modern style throughout this project.

---

# What is `Mapped[]`?

Look at this:

```python
id: Mapped[int]
```

Think of it as a special type hint.

You're telling SQLAlchemy:

> "This attribute is stored in the database and contains an integer."

Another example:

```python
username: Mapped[str]
```

Or:

```python
created_at: Mapped[datetime]
```

This improves:

* Autocomplete
* Type checking
* Readability

---

# What is `mapped_column()`?

`Mapped[]` tells SQLAlchemy **what type** the attribute is.

`mapped_column()` tells SQLAlchemy **how to store it**.

Example:

```python
id: Mapped[int] = mapped_column(primary_key=True)
```

Meaning:

* Integer
* Database column
* Primary Key

---

# Creating Our First Model

Create:

```text
app/models/user.py
```

```python
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
```

Don't just copy it.

Let's understand every line.

---

# `__tablename__`

```python
__tablename__ = "users"
```

SQLAlchemy now knows:

```text
Python Class

↓

User
```

maps to

```text
Database Table

↓

users
```

---

# Primary Key

```python
id: Mapped[int] = mapped_column(primary_key=True)
```

SQLAlchemy automatically creates:

```sql
id INTEGER PRIMARY KEY
```

For PostgreSQL, integer primary keys are auto-incrementing by default when configured this way.

---

# String Columns

```python
username: Mapped[str]
```

Means:

Python type:

```python
str
```

Database type:

```python
VARCHAR(100)
```

---

# `nullable=False`

Suppose someone creates:

```python
User(username=None)
```

Should that be allowed?

No.

```python
nullable=False
```

prevents NULL values.

---

# `unique=True`

```python
email: Mapped[str] = mapped_column(
    unique=True
)
```

Now PostgreSQL guarantees:

```
abc@gmail.com

↓

Only one user
```

Even if two people try registering simultaneously, the database enforces uniqueness.

---

# Why Store `password_hash` Instead of `password`?

Never store:

```text
password = "123456"
```

Instead:

```text
password_hash
```

Later,

we'll learn:

* Hashing
* Argon2
* Verification

This is why we named the field `password_hash` from day one.

---

# Timestamps

```python
created_at
```

Stores:

```
2026-07-11 15:42:10
```

Useful for:

* Registration date
* Analytics
* Sorting
* Auditing

---

# Why `datetime.utcnow`?

We pass the function:

```python
default=datetime.utcnow
```

Notice:

No parentheses.

SQLAlchemy calls it when creating a new row.

This ensures each user gets the current timestamp at creation time.

**Note:** In newer applications, many teams prefer timezone-aware timestamps. We'll revisit this later when we discuss production-ready date/time handling.

---

# Conversation Model

Create:

```text
app/models/conversation.py
```

```python
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship("User", back_populates="conversations")
```

---

# What is a Foreign Key?

Remember Lesson 5.

One user

↓

Many conversations

How does SQLAlchemy know?

```python
ForeignKey("users.id")
```

Meaning:

```
Conversation.user_id

↓

Users.id
```

Now every conversation belongs to one user.

---

# What is `relationship()`?

Foreign Keys connect tables **in the database**.

`relationship()` connects objects **in Python**.

Instead of:

```python
conversation.user_id
```

you can do:

```python
conversation.user
```

SQLAlchemy loads the related `User` object for you.

---

# Complete the User Relationship

Go back to `user.py`.

Add:

```python
from sqlalchemy.orm import relationship
```

Then inside the class:

```python
conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan",
)
```

Now:

```text
User

↓

Conversation

↓

Conversation

↓

Conversation
```

This is a **One-to-Many** relationship.

---

# Message Model

Create:

```text
app/models/message.py
```

```python
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    role: Mapped[str] = mapped_column(nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )
```

---

Update `conversation.py`:

```python
messages = relationship(
    "Message",
    back_populates="conversation",
    cascade="all, delete-orphan",
)
```

---

# Database Relationships

Our database now looks like this:

```text
User
│
├── id
├── username
├── email
└── password_hash
│
└──────────────┐
               │
               ▼
Conversation
│
├── id
├── title
└── user_id
│
└──────────────┐
               │
               ▼
Message
│
├── id
├── role
├── content
└── conversation_id
```

---

# Why Use `cascade="all, delete-orphan"`?

Imagine:

```
Delete User
```

Should the user's conversations remain?

No.

Likewise:

```
Delete Conversation
```

Should its messages remain?

No.

`cascade="all, delete-orphan"` ensures related child records are also removed, preventing orphaned data.

---

# Registering Models

Create:

```text
app/models/__init__.py
```

```python
from .conversation import Conversation
from .message import Message
from .user import User

__all__ = [
    "User",
    "Conversation",
    "Message",
]
```

Importing this module later ensures SQLAlchemy knows about all of our models before creating tables or running migrations.

---

# Why Haven't We Created Tables Yet?

We now have:

* Models
* Relationships
* Columns

But PostgreSQL still doesn't know about them.

We'll solve that in the next lesson using **Alembic**, which manages database schema changes through migrations.

---

# What You Learned Today

You now understand:

* What a Model is
* SQLAlchemy 2.0 model syntax
* `Mapped[]`
* `mapped_column()`
* `__tablename__`
* Primary Keys
* Foreign Keys
* `relationship()`
* One-to-Many relationships
* Timestamps
* Organizing models into separate files
* Why relationships exist in both the database and Python

---


