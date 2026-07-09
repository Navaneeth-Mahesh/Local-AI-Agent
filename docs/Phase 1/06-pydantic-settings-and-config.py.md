# Phase 1 — Lesson 5
# Building a Production-Ready Configuration System

---

# Learning Objectives

By the end of this lesson, you will be able to:

- Install `pydantic-settings`
- Create a centralized configuration system
- Understand every line of `config.py`
- Load environment variables automatically
- Validate configuration during startup
- Use type hints with configuration
- Import configuration anywhere in the project
- Understand why this approach is used in production applications

---

# Introduction

In the previous lesson, we learned why configuration management is important.

We also learned why secrets should never be hardcoded.

Now it's time to actually build our configuration system.

By the end of this lesson, we'll have a reusable configuration object that the entire application can use.

Instead of writing:

```python
import os

database_url = os.getenv("DATABASE_URL")
```

inside every file,

we'll simply write:

```python
from app.core.config import settings

print(settings.DATABASE_URL)
```

One import.

Anywhere.

That's exactly how professional FastAPI projects are built.

---

# Project Structure

Our backend now looks like this:

```text
backend/
│
├── app/
│   │
│   ├── api/
│   ├── core/
│   │     ├── config.py
│   │     ├── logging.py
│   │     └── security.py
│   │
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   │
│   └── main.py
│
├── .env
├── requirements.txt
└── .gitignore
```

The `core` directory contains infrastructure that every other module depends on.

One of those files is `config.py`.

---

# Step 1 — Install Pydantic Settings

Run the following command inside your virtual environment.

```bash
pip install pydantic-settings
```

Or install everything at once:

```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary pydantic-settings python-dotenv
```

---

# Why Do We Need Pydantic Settings?

Python already provides:

```python
import os

os.getenv("DATABASE_URL")
```

So why install another library?

Because `os.getenv()` only returns strings.

Example:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Using `os.getenv()`:

```python
minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
```

Result:

```
"30"
```

Notice something?

It's a **string**, not an integer.

You would have to convert it manually.

```python
minutes = int(os.getenv(...))
```

Now imagine doing that for:

- 25 configuration values
- Different data types
- Validation
- Default values

It quickly becomes repetitive.

Pydantic solves all of this automatically.

---

# Step 2 — Create the `.env` File

Inside the backend directory:

```text
backend/

.env
```

Example:

```env
PROJECT_NAME=Local AI Agent

DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_agent

JWT_SECRET=change_this_in_production

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

GEMINI_API_KEY=your_api_key_here

DEBUG=True
```

Notice that every value is stored as text.

Pydantic converts them into the correct Python types automatically.

---

# Step 3 — Create `config.py`

Create:

```text
app/
└── core/
      └── config.py
```

---

# The Complete Configuration Class

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str

    DATABASE_URL: str

    JWT_SECRET: str

    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REFRESH_TOKEN_EXPIRE_DAYS: int

    GEMINI_API_KEY: str

    DEBUG: bool

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
```

Let's understand every line.

---

# Import Statements

```python
from pydantic_settings import BaseSettings
```

`BaseSettings` is the foundation of our configuration class.

It knows how to:

- Read `.env`
- Read environment variables
- Validate types
- Create Python objects

Everything happens automatically.

---

```python
SettingsConfigDict
```

This class lets us configure how our settings behave.

Think of it as configuration for the configuration system.

---

# Creating the Settings Class

```python
class Settings(BaseSettings):
```

We're creating a normal Python class.

The difference is that it inherits from `BaseSettings`.

Because of this,

Pydantic automatically reads the environment variables.

---

# Defining Variables

```python
PROJECT_NAME: str
```

We're saying:

> PROJECT_NAME must exist, and it must be a string.

---

```python
DATABASE_URL: str
```

The database connection string.

---

```python
JWT_SECRET: str
```

The secret key used to sign JWT tokens.

---

```python
ACCESS_TOKEN_EXPIRE_MINUTES: int
```

Notice the type.

Even though `.env` stores:

```
30
```

as text,

Pydantic converts it into:

```python
30
```

an integer.

No manual conversion required.

---

```python
DEBUG: bool
```

Suppose `.env` contains:

```env
DEBUG=True
```

Pydantic automatically converts it into:

```python
True
```

a Boolean value.

---

# model_config

```python
model_config = SettingsConfigDict(
    env_file=".env",
    extra="ignore"
)
```

This tells Pydantic:

```
Look inside:

.env
```

for configuration values.

---

## What Does `extra="ignore"` Mean?

Suppose your `.env` contains:

```env
SOME_RANDOM_VARIABLE=123
```

But your class doesn't define it.

Without:

```python
extra="ignore"
```

Pydantic would complain.

With it,

unknown variables are simply ignored.

---

# Creating the Settings Object

Finally:

```python
settings = Settings()
```

This is the most important line.

It creates one global settings object.

Every module imports this object.

No module creates another Settings instance.

This gives us a **single source of truth**.

---

# What Happens Internally?

When Python executes:

```python
settings = Settings()
```

Pydantic performs several steps.

```
Read .env

↓

Find PROJECT_NAME

↓

Find DATABASE_URL

↓

Convert values

↓

Validate types

↓

Create Settings object

↓

Application starts
```

If something is missing,

the application immediately stops.

---

# Startup Validation

Suppose you accidentally delete:

```env
DATABASE_URL
```

When the application starts,

Pydantic immediately raises an error.

```
ValidationError

DATABASE_URL

Field required
```

Instead of failing later,

it fails immediately.

This is called **Fail Fast**.

Professional software prefers failing early.

---

# Accessing Configuration

Anywhere in the project:

```python
from app.core.config import settings
```

Now:

```python
print(settings.PROJECT_NAME)
```

Result:

```
Local AI Agent
```

---

```python
print(settings.DEBUG)
```

Result:

```
True
```

Notice that it's a Boolean,

not a string.

---

```python
print(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
```

Result:

```
30
```

Again,

an integer.

---

# Why This Is Better Than `os.getenv()`

Without Pydantic:

```python
os.getenv()

os.getenv()

os.getenv()

os.getenv()

os.getenv()
```

Repeated everywhere.

---

With Pydantic:

```
Settings()

↓

Validated

↓

Imported Everywhere
```

Cleaner.

Safer.

More maintainable.

---

# How Configuration Flows Through Our Application

Imagine a user logs in.

```
React

↓

POST /auth/login

↓

API Route

↓

Auth Service

↓

settings.JWT_SECRET

↓

Generate JWT

↓

Return Token
```

The Auth Service doesn't know where the secret came from.

It simply imports `settings`.

The same happens for:

- Database connections
- Gemini API
- Logging
- Redis
- Background jobs

Everything uses the same configuration object.

---

# Best Practices

Always follow these rules:

- Keep all configuration in one file.
- Never hardcode secrets.
- Use meaningful variable names.
- Validate configuration at startup.
- Import the global `settings` object instead of creating new ones.
- Never commit `.env` to GitHub.

---

# Key Takeaways

After this lesson, you should understand:

- `BaseSettings` loads environment variables automatically.
- Pydantic converts strings into proper Python types.
- Validation happens during application startup.
- A single `settings` object becomes the application's source of truth.
- Every module imports the same configuration object.
- This pattern is used in production FastAPI applications because it is clean, maintainable, and secure.

---

# What's Next?

Our configuration system is now complete.

The next step is connecting our application to a real PostgreSQL database.

We'll learn:

- What SQL is
- Why PostgreSQL is used
- How SQLAlchemy works
- What an ORM is
- How to create a database engine
- How sessions work
- How applications communicate with databases

This is where our backend begins storing real data.