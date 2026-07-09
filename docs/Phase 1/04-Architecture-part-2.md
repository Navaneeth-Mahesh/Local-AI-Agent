# Phase 1 — Lesson 3 (Part 2)
# Understanding Backend Layers

---

# Learning Objectives

By the end of this lesson, you will understand:

- Why backend applications are divided into layers
- What each layer is responsible for
- The API Layer
- The Service Layer
- The Repository Layer
- Database Models
- Schemas (DTOs)
- How a request travels through the application
- Why this architecture scales to large applications

---

# Introduction

In Part 1, we learned that large software projects need structure.

We also learned about the **Single Responsibility Principle (SRP)**, which teaches us that every part of our application should have one clear responsibility.

Now it's time to see how professional backend applications are actually organized.

Instead of writing everything inside our API routes, we'll divide our application into multiple layers.

Each layer has one responsibility and communicates only with the layers it needs.

This approach is called **Layered Architecture**, and it's one of the most common designs used in modern backend development.

---

# The Big Picture

Every request in our AI Agent will follow this path:

```text
                Client (React)
                     │
                     ▼
               API Layer
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

For AI features, the Service Layer may also communicate with external services:

```text
                Client
                    │
                    ▼
               API Layer
                    │
                    ▼
             Service Layer
              │            │
              ▼            ▼
       Repository      Gemini API
              │
              ▼
        PostgreSQL
```

Each layer has a different job.

Let's study them one by one.

---

# The API Layer

## What is the API Layer?

The API Layer is the **entry point** of our backend.

Every request from the frontend arrives here first.

Think of it as the **reception desk** of a hospital.

Patients don't walk directly into the operating room.

Instead, they first visit reception.

The receptionist:

- Greets the patient
- Collects information
- Verifies details
- Sends them to the correct department

The receptionist doesn't perform surgery.

Similarly, the API Layer doesn't contain business logic.

Its job is simply to receive requests and forward them.

---

## Responsibilities of the API Layer

The API Layer should:

- Receive HTTP requests
- Validate request data
- Authenticate the user
- Call the correct service
- Return an HTTP response

That's it.

Nothing more.

---

## What Should NOT Be Here?

Many beginners write code like this:

```python
@app.post("/register")
def register():

    validate_email()

    hash_password()

    save_user()

    send_email()

    generate_token()

    return response
```

This works.

But it's bad architecture.

The API route is doing too many jobs.

If registration logic changes, we'll need to modify the route itself.

Instead, the route should stay small.

---

## Professional Approach

```python
@app.post("/register")
def register(user: UserCreate):

    return auth_service.register(user)
```

That's much cleaner.

The API only delegates the work.

---

# Why Keep Routes Small?

Imagine your application has:

- 200 API endpoints
- 20 developers

If every route contains business logic, debugging becomes extremely difficult.

Small routes are easier to:

- Read
- Test
- Review
- Maintain

Professional API routes are intentionally boring.

Most of the interesting work happens elsewhere.

---

# The Service Layer

## What is the Service Layer?

The Service Layer is the **brain** of the application.

This is where all business rules live.

Business logic answers questions like:

- Can this user register?
- Is the email already taken?
- Should this user have access?
- Should memory be updated?
- Which AI provider should be used?
- Should a file be deleted?

Every important decision happens here.

---

# Example

Imagine a user registers.

The Service Layer might perform:

```text
Receive User

↓

Check Email Format

↓

Check Email Exists

↓

Hash Password

↓

Create User

↓

Generate JWT

↓

Send Welcome Email

↓

Return Response
```

Notice something.

None of this belongs in the API route.

---

# Why Business Logic Doesn't Belong in Routes

Suppose we later build:

- Web API
- Mobile App
- Desktop App

All three need registration.

If the logic is inside the API route, we'll duplicate it.

Instead:

```
React

↓

Service

Mobile

↓

Service

Desktop

↓

Service
```

Everyone shares the same business logic.

Only the frontend changes.

---

# Repository Layer

## What is a Repository?

Repositories are responsible for talking to the database.

Nothing else.

Think of a librarian.

When you ask for a book,

the librarian doesn't write the book.

They simply retrieve it.

Repositories work the same way.

---

# Responsibilities

Repositories:

- Insert data
- Update data
- Delete data
- Query data

They should NOT:

- Validate passwords
- Generate JWT
- Call Gemini
- Send emails

Those belong to the Service Layer.

---

# Example

Instead of:

```python
session.add(user)

session.commit()

session.refresh(user)
```

inside our service,

we write:

```python
user_repository.create(user)
```

Now our service doesn't care how the database works.

---

# Why Use Repositories?

Imagine today we're using PostgreSQL.

One day the company decides to migrate to MongoDB.

What changes?

Only the repository.

Everything else continues working.

This separation makes the application much easier to maintain.

---

# Database Models

## What is a Model?

A model represents a database table.

Imagine the Users table.

```
Users

------------------------

id

email

password_hash

created_at

updated_at
```

In Python, we represent this table using a class.

Each object represents one row.

```
User

↓

id

email

password_hash

created_at
```

The model defines how data is stored.

Nothing more.

---

# Why Models Exist

Instead of writing SQL everywhere,

we interact with Python objects.

Example:

Instead of saying:

```
INSERT INTO users...
```

we simply create a User object.

The ORM converts it into SQL automatically.

This makes our code cleaner and easier to understand.

---

# Schemas

One of the biggest beginner mistakes is using the database model everywhere.

Professional applications never do this.

Instead, they introduce **Schemas**.

---

# What is a Schema?

A schema defines the shape of data entering or leaving our API.

Think of it as a contract.

It tells FastAPI exactly what data is expected.

---

# Example

User registration requires:

```json
{
    "email":"abc@gmail.com",
    "password":"12345678"
}
```

This becomes:

```
UserCreate
```

---

After registration,

the frontend doesn't need the password anymore.

Instead, we return:

```json
{
    "id":1,
    "email":"abc@gmail.com"
}
```

This becomes:

```
UserResponse
```

Notice something important.

The password disappeared.

Schemas protect sensitive information.

---

# Why Not Return Models Directly?

Imagine returning this:

```json
{
    "id":1,
    "email":"abc@gmail.com",
    "password_hash":"$2b$12$..."
}
```

Huge security problem.

Clients should never see password hashes.

Schemas solve this problem.

---

# Request Lifecycle

Let's follow a real request.

A user clicks Register.

```
User

↓

React

↓

POST /auth/register
```

The request reaches FastAPI.

```
API Layer
```

The route validates the input.

Then:

```
Service Layer
```

The service:

- Validates email
- Hashes password
- Calls repository

↓

```
Repository Layer
```

Repository saves data.

↓

```
PostgreSQL
```

Database stores the new user.

↓

Repository returns the user.

↓

Service creates response.

↓

API Layer returns JSON.

↓

React receives response.

↓

User sees:

"Registration Successful"
```

This entire process usually takes less than a second.

---

# Complete Flow Diagram

```text
                User
                  │
                  ▼
          React Frontend
                  │
        HTTP POST /register
                  │
                  ▼
          FastAPI Route
                  │
                  ▼
        Authentication Service
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
 Hash Password        Validate Email
        │
        ▼
      Repository
        │
        ▼
 PostgreSQL Database
        │
        ▼
 Repository Returns User
        │
        ▼
 Authentication Service
        │
        ▼
 API Route
        │
        ▼
 JSON Response
        │
        ▼
 React UI
```

---

# How This Helps Our AI Agent

Our AI Agent will eventually support:

- Chat
- Memory
- File Search
- Browser Tools
- Plugins
- Voice
- Permissions
- RAG
- Local Models

Without layered architecture,

everything would become tangled together.

Instead, each feature gets its own place.

For example:

```
AI Routes

↓

AI Service

↓

Gemini Client
```

Memory:

```
Memory Routes

↓

Memory Service

↓

Memory Repository

↓

PostgreSQL
```

File Search:

```
File Routes

↓

Search Service

↓

Vector Database
```

Every feature follows the same pattern.

Once you understand one module,

you'll understand the rest.

---

# Benefits of Layered Architecture

Following this architecture gives us many advantages.

### Easier Maintenance

Every responsibility has its own location.

---

### Easier Testing

Each layer can be tested independently.

---

### Easier Teamwork

Developers can work on different layers without interfering with each other.

---

### Better Scalability

New features can be added without rewriting existing code.

---

### Better Code Reuse

Business logic can be reused by multiple clients.

---

### Cleaner Code

Small, focused modules are much easier to understand.

---

# Key Takeaways

After this lesson, you should understand:

- API Routes receive requests.
- Services contain business logic.
- Repositories communicate with the database.
- Models represent database tables.
- Schemas define API request and response data.
- Each layer has a single responsibility.
- Layered Architecture keeps large applications maintainable and scalable.

---

# What's Next?

In the next lesson, we'll move beyond architecture and learn how professional applications manage configuration.

You'll learn:

- What configuration management is
- Why secrets should never be hardcoded
- What environment variables are
- How `.env` files work
- How Pydantic Settings loads configuration
- Why centralized configuration is considered a best practice

This will become the foundation that every other part of our AI Agent relies on.