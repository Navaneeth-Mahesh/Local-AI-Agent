# Phase 1 — Lesson 4
# Configuration Management & Environment Variables

---

# Learning Objectives

By the end of this lesson, you will understand:

- What configuration management is
- Why configuration should be separated from code
- What environment variables are
- Why hardcoding secrets is dangerous
- What a `.env` file is
- How FastAPI reads configuration
- What Pydantic Settings is
- Why centralized configuration is considered a best practice
- How configuration fits into our AI Agent architecture

---

# Introduction

Imagine you've spent months building your AI Agent.

Everything works perfectly on your computer.

Your project contains:

- User Authentication
- AI Chat
- PostgreSQL Database
- JWT Authentication
- Gemini API
- Logging
- Background Tasks

Now it's time to deploy it to a cloud server.

You upload your project.

Run the application.

And immediately...

```
Database Connection Failed
```

Then you fix it.

Next error.

```
Gemini API Key Invalid
```

Fix that.

Next error.

```
JWT Secret Missing
```

Why?

Because your application was written specifically for **your computer**.

Professional software should run on:

- Your laptop
- Another developer's laptop
- Testing server
- Production server
- Docker container

Without changing a single line of code.

This is where **Configuration Management** comes in.

---

# What is Configuration?

Before learning configuration management,

let's first understand what configuration actually means.

Configuration simply means:

> Values that control how an application behaves without changing its source code.

Think of configuration as **settings**.

For example:

A video game has settings like:

- Volume
- Brightness
- Resolution
- Language

The game itself doesn't change.

Only the settings do.

Software works exactly the same way.

---

# Examples of Configuration

Our AI Agent will need many configurable values.

For example:

```
Database URL

postgresql://localhost/ai_agent
```

---

```
Gemini API Key

AIza....
```

---

```
JWT Secret

my-super-secret-key
```

---

```
Access Token Lifetime

30 minutes
```

---

```
Application Name

Local AI Agent
```

---

Notice something.

These values are **not part of our business logic**.

They are simply settings.

---

# What is Configuration Management?

Configuration Management is the practice of storing and managing application settings separately from the source code.

Instead of writing values directly inside Python files,

we store them somewhere else.

Our application loads them when it starts.

This gives us flexibility.

---

# Why Not Hardcode Values?

Suppose you write:

```python
DATABASE_URL = "postgresql://postgres:password@localhost/ai_agent"

JWT_SECRET = "super_secret_key"

GEMINI_API_KEY = "AIzaSy..."
```

Everything works.

So what's the problem?

Let's look at several problems.

---

# Problem 1 — Security

Imagine pushing your project to GitHub.

Your repository now contains:

```
JWT Secret

Database Password

Gemini API Key
```

Anyone can see them.

Someone could:

- Use your AI API
- Connect to your database
- Generate fake JWT tokens

Your entire application becomes vulnerable.

This is one of the most common beginner mistakes.

---

# Problem 2 — Different Computers

Imagine three developers working together.

Developer A

```
Database

localhost
```

Developer B

```
Database

192.168.1.50
```

Developer C

```
Database

Docker Container
```

Should everyone modify the source code?

No.

The code should remain identical.

Only the configuration should change.

---

# Problem 3 — Multiple Environments

Professional software usually has multiple environments.

For example:

```
Development
```

Used while writing code.

---

```
Testing
```

Used for automated tests.

---

```
Production
```

Used by real users.

Each environment needs different settings.

Example:

Development

```
Database

localhost
```

Production

```
Database

AWS PostgreSQL
```

Same application.

Different configuration.

---

# What Are Environment Variables?

An Environment Variable is simply a variable provided by the operating system.

Instead of storing configuration inside Python,

the operating system stores it.

Your application asks the operating system for the value.

Conceptually:

```
Operating System

↓

DATABASE_URL

↓

Application
```

Your application doesn't care where the value came from.

It simply asks:

> "What is the database URL?"

The operating system answers.

---

# Why Environment Variables?

Environment variables allow us to:

- Keep secrets out of source code
- Use different settings on different machines
- Deploy the same application everywhere
- Improve security

This is why nearly every modern backend framework supports them.

---

# The `.env` File

Typing environment variables manually every time would be inconvenient.

Instead, during development,

we store them in a file called:

```
.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost/ai_agent

JWT_SECRET=my_super_secret_key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

GEMINI_API_KEY=your_api_key_here
```

Notice something important.

This is **not Python code**.

It's simply:

```
KEY=VALUE
```

pairs.

---

# How Does the Application Read `.env`?

When our application starts,

Pydantic Settings reads the `.env` file.

```
.env

↓

Pydantic Settings

↓

Python Objects

↓

Application
```

After that,

our application can access configuration anywhere.

---

# Why Don't We Import `.env` Directly?

Imagine every file doing this:

```
main.py

↓

Read .env
```

---

```
login.py

↓

Read .env
```

---

```
chat.py

↓

Read .env
```

---

```
database.py

↓

Read .env
```

Every file repeats the same work.

This creates duplication.

Instead,

we load configuration once.

---

# Centralized Configuration

Professional applications use a single configuration object.

```
config.py

↓

Load .env

↓

Create Settings Object

↓

Everyone imports settings
```

Now every module shares the same configuration.

This is called a **Single Source of Truth**.

---

# What is Pydantic Settings?

Pydantic Settings is a library that automatically converts environment variables into Python objects.

Instead of writing:

```python
import os

database = os.getenv("DATABASE_URL")

secret = os.getenv("JWT_SECRET")

api_key = os.getenv("GEMINI_API_KEY")
```

again and again,

we define everything in one place.

Conceptually:

```python
class Settings:

    DATABASE_URL

    JWT_SECRET

    GEMINI_API_KEY
```

Pydantic automatically loads the values.

It also validates their types.

---

# Why Is Validation Important?

Suppose we expect:

```
ACCESS_TOKEN_EXPIRE_MINUTES

↓

Integer
```

But someone accidentally writes:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=Thirty
```

Without validation,

the application might fail much later.

With Pydantic,

the application immediately reports the error during startup.

Finding mistakes early is much easier.

---

# Why Centralized Configuration Is Better

Without centralized configuration:

```
main.py

↓

os.getenv()

↓

auth.py

↓

os.getenv()

↓

database.py

↓

os.getenv()

↓

chat.py

↓

os.getenv()
```

Configuration is scattered throughout the project.

Now imagine changing a variable name.

You must update every file.

Instead:

```
config.py

↓

Load once

↓

Create Settings

↓

Import Everywhere
```

Cleaner.

Safer.

Much easier to maintain.

---

# Where Will Configuration Live?

Our backend structure now looks like this:

```text
backend/

app/

├── api/
├── services/
├── repositories/
├── database/
├── models/
├── schemas/

├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py

└── main.py

.env

.gitignore
```

The `core` package contains infrastructure shared by the entire application.

Every module imports configuration from here.

---

# Real Example in Our AI Agent

Imagine a user sends a message:

> "Summarize this PDF."

What happens?

```
User

↓

React

↓

FastAPI

↓

AI Service

↓

Read Gemini API Key

↓

Connect to Gemini

↓

Receive Response

↓

Return to User
```

Notice something.

The AI Service never needs to know where the API key came from.

It simply asks the configuration system.

This keeps our code clean and secure.

---

# Why `.env` Should Never Be Uploaded

Imagine someone downloads your GitHub repository.

If your `.env` file is included,

they instantly receive:

- Database credentials
- JWT secrets
- API keys
- Email passwords
- Cloud credentials

This is why every Python project includes:

```text
.env

.venv/

__pycache__/

.pytest_cache/
```

inside `.gitignore`.

---

# Best Practices

Always follow these rules:

- Never hardcode secrets.
- Never upload `.env` files to GitHub.
- Keep all configuration in one place.
- Validate configuration during startup.
- Use meaningful environment variable names.
- Treat secrets like passwords.

---

# Key Takeaways

After this lesson, you should understand:

- Configuration controls how an application behaves.
- Configuration should be separate from source code.
- Environment variables allow different machines to use different settings.
- `.env` files simplify local development.
- Pydantic Settings loads and validates configuration.
- Centralized configuration creates a single source of truth.
- Secrets should never be committed to Git.

---

# What's Next?

In the next lesson, we'll stop discussing theory and begin writing production-ready code.

We'll:

- Install `pydantic-settings`
- Create `app/core/config.py`
- Build our `Settings` class
- Load values from `.env`
- Validate configuration automatically
- Understand type hints in configuration classes
- Use our configuration throughout the application

By the end of the next lesson, our backend will have its first reusable infrastructure component—one that every future module will depend on.