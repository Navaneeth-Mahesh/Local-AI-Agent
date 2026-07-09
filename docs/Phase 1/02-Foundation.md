# Foundation

# Phase 1 —> Lesson 2
# Project Setup & Development Environment

---

# Learning Objectives

By the end of this lesson, you will have:

- A professional project folder structure
- A Git repository
- A Python virtual environment
- FastAPI installed
- Uvicorn installed
- A running FastAPI server
- Automatic Swagger API documentation
- A clear understanding of every file and folder we create

This lesson is the foundation of our entire AI Agent project. Everything we build in the future—authentication, databases, AI integration, memory, and tools—will be added to this foundation.

---

# Project Vision

We're not building a simple tutorial project.

We're building a production-grade AI Agent that anyone can run on their own computer.

By the end of this project, our application will include:

- User Authentication
- AI Chat
- Conversation History
- Long-Term Memory
- Local File Search
- Document Search (RAG)
- Tool Calling
- Browser Automation
- Local Computer Permissions
- Plugin System
- Settings
- Multi-user Support

To make the project easy to maintain, we'll organize everything from the beginning.

---

# Step 1 — Create the Project Folder

Create a folder anywhere on your computer.

Example:

```text
AI-Agent/
```

Inside it, create the following structure:

```text
AI-Agent/
│
├── backend/
│
├── frontend/
│
├── docs/
│
├── docker/
│
├── tests/
│
└── README.md
```

---

# Understanding the Project Structure

Instead of putting every file into one folder, professional applications separate different parts of the project.

Each folder has a single responsibility.

---

## backend/

This folder contains everything related to the server.

Examples:

- FastAPI
- Database
- Authentication
- AI Integration
- Memory System
- Business Logic
- APIs

Think of it as the **brain** of the application.

---

## frontend/

This folder contains everything the user interacts with.

Examples:

- React
- Tailwind CSS
- Chat Interface
- Dashboard
- Settings Page
- Authentication Pages

Think of it as the **face** of the application.

---

## docs/

Documentation for the project.

Later we'll store:

- Architecture diagrams
- API documentation
- Development notes
- Learning notes
- Design decisions

Good documentation makes projects easier to understand and maintain.

---

## tests/

Contains automated tests.

Instead of manually testing every feature, we'll write tests that verify our application works correctly.

Production code and test code should always remain separate.

---

## docker/

Contains Docker-related files.

Later this folder will include:

- Dockerfile
- docker-compose.yml

Docker allows our application to run consistently on any computer.

---

## README.md

The first file people see when they visit your GitHub repository.

It usually contains:

- Project overview
- Features
- Installation steps
- Technologies used
- Screenshots
- Usage instructions

A good README makes your project look professional.

---

# Step 2 — Initialize Git

Open VS Code.

Open the **AI-Agent** folder.

Open the integrated terminal.

Run:

```bash
git init
```

---

# What is Git?

Git is a Version Control System.

It records every change you make to your project.

Think of Git as a time machine.

Without Git:

```text
project/

main.py

main_old.py

main_new.py

main_final.py

main_final_final.py

main_really_final.py
```

Almost every beginner eventually creates files like these.

---

With Git:

```text
Commit 1

↓

Commit 2

↓

Commit 3

↓

Commit 4
```

Every change is saved.

If something breaks, you can return to any previous version.

---

# Why Do Developers Use Git?

Git allows us to:

- Track every change
- Undo mistakes
- Collaborate with other developers
- Experiment safely
- Maintain project history

Throughout this project, we'll commit our progress after completing each feature.

---

# Step 3 — Move into the Backend Folder

Navigate into the backend directory.

```bash
cd backend
```

All backend development will happen inside this folder.

---

# Step 4 — Create a Virtual Environment

Run:

### Windows

```bash
python -m venv .venv
```

---

# What is a Virtual Environment?

A Virtual Environment is an isolated Python environment for a specific project.

Instead of sharing packages across every project, each project gets its own independent environment.

---

## Without a Virtual Environment

Imagine your computer has one global Python installation.

```text
Computer

↓

Python

↓

FastAPI

↓

Flask

↓

Django

↓

SQLAlchemy

↓

Requests
```

Every project shares the same packages.

Now imagine:

Project A requires:

```
FastAPI 0.115
```

Project B requires:

```
FastAPI 0.118
```

Both versions cannot exist globally without causing conflicts.

---

## With a Virtual Environment

Each project gets its own isolated environment.

```text
Project A

↓

Python

↓

FastAPI 0.115

↓

Other Packages
```

---

```text
Project B

↓

Python

↓

FastAPI 0.118

↓

Other Packages
```

The projects no longer interfere with each other.

This isolation is one of the most important concepts in Python development.

---

# Why is the Folder Named `.venv`?

The name `.venv` is simply a convention.

The leading dot makes it a hidden folder on many operating systems.

Inside this folder, Python stores:

- A private interpreter
- Installed packages
- Scripts
- Configuration files

You should never edit these files manually.

---

# Step 5 — Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate
```

---

If activation is successful, you'll see:

```text
(.venv)
PS C:\AI-Agent\backend>
```

The `(.venv)` indicates that your terminal is now using the project's isolated Python environment.

Every package you install from now on will only affect this project.

---

# Step 6 — Install FastAPI and Uvicorn

Run:

```bash
pip install fastapi uvicorn
```

---

# Understanding `pip`

`pip` is Python's package manager.

It downloads and installs libraries from the Python Package Index (PyPI).

Whenever you need a third-party library, you'll typically install it using `pip`.

Example:

```bash
pip install package-name
```

---

# What Did We Install?

## FastAPI

FastAPI is a modern Python web framework for building APIs.

It provides:

- URL routing
- Request handling
- Response generation
- Data validation
- Automatic documentation
- JSON serialization

Without FastAPI, we'd need thousands of lines of networking code.

FastAPI handles all of that for us.

---

## Uvicorn

FastAPI describes **how** requests should be handled.

Uvicorn is responsible for **running** the application.

Think of it like this:

```text
FastAPI

↓

Knows what to do
```

```text
Uvicorn

↓

Keeps waiting for requests
```

Without Uvicorn, FastAPI cannot receive HTTP requests.

---

# Step 7 — Save Project Dependencies

Run:

```bash
pip freeze > requirements.txt
```

---

# What is `requirements.txt`?

Every project depends on external libraries.

Instead of asking someone to guess which packages are required, we list them in one file.

Example:

```text
fastapi==0.xx.x

uvicorn==0.xx.x
```

This file ensures everyone uses the same package versions.

---

## Why is This Important?

Imagine someone clones your GitHub repository.

Instead of manually installing packages one by one, they simply run:

```bash
pip install -r requirements.txt
```

Python installs every required dependency automatically.

This guarantees consistent environments across different computers.

---

# Step 8 — Create the Backend Structure

Inside the `backend` folder, create:

```text
backend/
│
├── app/
├── requirements.txt
└── .env
```

---

Now create the following folders inside `app/`.

```text
app/
│
├── api/
├── core/
├── database/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/
└── main.py
```

Don't worry if some folders are empty for now.

We'll build each one as the project grows.

---

# Understanding the Backend Structure

Professional applications separate responsibilities into different layers.

This keeps the project organized and easier to maintain.

---

## api/

Contains API endpoints.

Examples:

```text
POST /auth/login

POST /auth/register

GET /users/me

POST /chat
```

These files receive HTTP requests and return responses.

They should contain very little business logic.

---

## services/

Contains business logic.

Example:

```text
User Registers

↓

Validate Data

↓

Hash Password

↓

Create User

↓

Return Response
```

The service layer decides **what should happen**.

---

## repositories/

Responsible for interacting with the database.

Instead of writing SQL inside API routes, repositories handle:

- Insert
- Update
- Delete
- Search

This separation makes the code cleaner and easier to test.

---

## models/

Contains database models.

Each model usually represents one database table.

Examples:

```text
User

Conversation

Message

Memory
```

Later, SQLAlchemy will use these models to generate database tables.

---

## schemas/

Defines the structure of data entering and leaving our API.

Example:

Registration Request:

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

Registration Response:

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

Notice that the password is **never returned**.

Schemas help validate and protect our data.

---

## database/

Contains:

- Database connection
- Session management
- Database configuration

Instead of connecting to PostgreSQL everywhere, we'll centralize it here.

---

## core/

Contains global application configuration.

Later it will include:

- Environment variables
- JWT settings
- Security configuration
- Application settings

Think of it as the central configuration folder.

---

## utils/

Contains reusable helper functions.

Examples:

- Date formatting
- String utilities
- File helpers
- Common functions

These utilities can be reused across multiple parts of the application.

---

# Step 9 — Create `main.py`

Create:

```text
backend/
└── app/
    └── main.py
```

Add the following code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Agent Backend"
    }
```

---

# Understanding Every Line

## Import FastAPI

```python
from fastapi import FastAPI
```

We're importing the `FastAPI` class from the `fastapi` package.

Before we can create a web application, Python needs to know what `FastAPI` is.

---

## Create the Application

```python
app = FastAPI()
```

This creates our FastAPI application.

Everything in our backend—routes, middleware, events, and configuration—will be attached to this `app` object.

Think of it as the heart of the application.

---

## Route Decorator

```python
@app.get("/")
```

This line tells FastAPI:

> "When a client sends a GET request to `/`, run the function immediately below."

The `@` symbol introduces a **decorator**.

Decorators modify or extend the behavior of functions.

We'll study decorators in detail later.

For now, think of them as labels that connect URLs to Python functions.

---

## Endpoint Function

```python
def home():
```

This function runs whenever someone visits:

```
http://127.0.0.1:8000/
```

---

## Return Statement

```python
return {
    "message": "Welcome to AI Agent Backend"
}
```

This is a normal Python dictionary.

FastAPI automatically converts it into JSON.

Python:

```python
{
    "message": "Welcome"
}
```

Response:

```json
{
  "message": "Welcome"
}
```

You don't need to manually convert dictionaries into JSON.

FastAPI does that automatically.

---

# Step 10 — Run the Server

From the `backend` folder, run:

```bash
uvicorn app.main:app --reload
```

---

# Understanding the Command

```bash
uvicorn
```

Starts the Uvicorn server.

---

```bash
app.main
```

Refers to the Python module:

```text
app/main.py
```

---

```bash
:app
```

Refers to the FastAPI application object.

```python
app = FastAPI()
```

---

```bash
--reload
```

Automatically restarts the server whenever you save changes.

This is very useful during development because you don't need to restart the server manually after every code change.

---

# Step 11 — Open Your Browser

Visit:

```
http://127.0.0.1:8000
```

You should see:

```json
{
  "message": "Welcome to AI Agent Backend"
}
```

Congratulations!

You've successfully created and run your first FastAPI application.

---

# Step 12 — Automatic API Documentation

One of FastAPI's most powerful features is automatic API documentation.

Open:

```
http://127.0.0.1:8000/docs
```

You'll see an interactive Swagger UI.

From here, you can:

- View all available endpoints
- Read endpoint descriptions
- Test APIs directly in the browser
- View request and response formats

As our project grows, this page will automatically update with every new API we create.

---

# Request Flow

Let's visualize what happens when you visit the homepage.

```text
Browser

↓

HTTP GET /

↓

Uvicorn receives the request

↓

FastAPI matches the "/" route

↓

home() function executes

↓

Python returns a dictionary

↓

FastAPI converts it to JSON

↓

Browser displays the response
```

This simple flow is the foundation of every API we'll build.

---

# Key Takeaways

After completing this lesson, you now understand:

- How to organize a professional project
- Why we separate backend, frontend, documentation, and tests
- What Git is and why version control matters
- What a Python virtual environment is
- Why dependency isolation is important
- What `pip` does
- What `requirements.txt` is used for
- How a FastAPI application is created
- How routing works
- What decorators do at a high level
- How Python dictionaries become JSON responses
- How Uvicorn runs a FastAPI application
- How to start a development server
- How FastAPI automatically generates interactive API documentation

---

# What's Next?

In the next lesson, we'll begin building a real backend by learning:

- Application configuration
- Environment variables
- The `.env` file
- Pydantic Settings
- Configuration management
- Keeping secrets out of our source code

These concepts will prepare us for connecting databases, authentication, and AI providers securely.