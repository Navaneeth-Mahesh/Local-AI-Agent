# Backend Architecture

As our AI Agent grows, we don't want all the code to be written in a single file. Instead, we divide the application into multiple layers, where each layer has **one clear responsibility**.

This design makes the project easier to understand, maintain, test, and scale.

Our backend architecture looks like this:

```text
Frontend
    │
    ▼
API Routes
    │
    ▼
Services
    │
    ▼
Repositories
    │
    ▼
SQLAlchemy Models
    │
    ▼
PostgreSQL Database
```

Let's understand each layer.

---

# 1. Frontend

The frontend is the part of the application that users interact with.

In our project, the frontend will be built using **React**.

It is responsible for:

- Displaying the user interface
- Sending HTTP requests
- Receiving API responses
- Showing AI conversations
- Managing user interactions

The frontend **does not** contain business logic or communicate directly with the database or AI provider.

Example:

```
User types:

"Explain Python decorators."
```

The frontend simply sends that request to the backend.

---

# 2. API Routes

API Routes are the entry point of the backend.

They receive requests from the frontend and return responses.

Example:

```http
POST /auth/register

POST /auth/login

GET /users/me

POST /chat
```

Routes should remain **very small**.

Their responsibilities include:

- Receiving HTTP requests
- Validating input using schemas
- Calling the appropriate service
- Returning the response

Routes should **not** contain business logic or database queries.

Think of routes as receptionists—they receive requests and forward them to the correct department.

---

# 3. Services

The Service Layer contains the application's **business logic**.

This is where the application decides **how** something should happen.

For example, when a user registers, the service will:

```
Receive user data

↓

Check if the email already exists

↓

Hash the password

↓

Create a new user

↓

Save the user

↓

Return the response
```

Services coordinate different parts of the application.

They may call:

- Repositories
- Authentication utilities
- AI providers
- External APIs

Services should not know how the database works internally.

---

# 4. Repositories

Repositories are responsible for communicating with the database.

Instead of writing SQL queries inside routes or services, we keep all database operations in repository classes.

Examples:

- Create a user
- Find a user by email
- Update a profile
- Delete a conversation

Example flow:

```
Service

↓

Repository

↓

Database
```

This keeps database code organized in one place.

If we ever change databases, only the repository layer needs to be updated.

---

# 5. SQLAlchemy Models

Models represent database tables as Python classes.

Instead of writing raw SQL like:

```sql
SELECT * FROM users;
```

we work with Python objects.

Example:

```python
user.username
user.email
```

A model defines:

- Table name
- Columns
- Data types
- Relationships
- Constraints

Example:

```
User

├── id
├── username
├── email
├── password_hash
├── created_at
└── updated_at
```

Models are used internally by the backend and are never exposed directly to the frontend.

---

# 6. PostgreSQL Database

The database is where application data is stored permanently.

Examples of stored data include:

- User accounts
- Password hashes
- Conversations
- AI memory
- User settings
- Refresh tokens

Think of the database as the application's long-term memory.

Whenever the application restarts, the data remains safe because it is stored in PostgreSQL.

---

# Complete Request Flow

When a user logs in, the request flows through every layer.

```text
Frontend

↓

POST /auth/login

↓

API Route

↓

Authentication Service

↓

User Repository

↓

SQLAlchemy User Model

↓

PostgreSQL Database

↓

User Repository

↓

Authentication Service

↓

API Route

↓

Frontend
```

Each layer performs a specific responsibility before passing the data to the next layer.

---

# Project Layers

Our backend is divided into several logical layers.

## Routes

- Receive HTTP requests
- Validate request data
- Call services
- Return HTTP responses

Routes should remain thin and contain almost no business logic.

---

## Services

- Business logic
- Application rules
- AI integration
- Authentication logic
- Permission handling

Services are the "brain" of the backend.

---

## Repositories

- Read data
- Insert data
- Update data
- Delete data

Repositories are the only layer responsible for communicating with the database.

---

## Database

The database stores all persistent application data.

Examples include:

- Users
- Conversations
- Memory
- API keys
- Settings

---

## Models

Models define the structure of database tables using SQLAlchemy.

Each model represents one table in PostgreSQL.

Examples:

- User
- Conversation
- Message

---

## Schemas

Schemas define the structure of data entering and leaving the application.

They are responsible for:

- Input validation
- Output serialization
- Automatic documentation
- Type checking

Schemas are used for API communication, not database storage.

---

# Software Design Principles

To keep our project scalable and maintainable, we'll follow several important software engineering principles.

---

# Clean Architecture

Clean Architecture organizes code into independent layers.

Each layer has a single responsibility and depends only on the layers beneath it.

```text
Routes

↓

Services

↓

Repositories

↓

Database
```

### Benefits

- Easier to understand
- Easier to maintain
- Easier to test
- Easier to replace components
- Better scalability

---

# SOLID Principles

SOLID is a set of five object-oriented design principles that help us write clean, flexible, and maintainable code.

## S — Single Responsibility Principle (SRP)

A class should have only one reason to change.

Example:

A `UserRepository` should only manage database operations.

It should **not** send emails or generate JWT tokens.

---

## O — Open/Closed Principle (OCP)

Software should be open for extension but closed for modification.

Instead of changing existing code, we extend it by adding new classes or features.

---

## L — Liskov Substitution Principle (LSP)

A child class should be able to replace its parent class without breaking the application.

This makes inheritance predictable and safe.

---

## I — Interface Segregation Principle (ISP)

Classes should not be forced to implement methods they don't need.

Instead of creating one large interface, we create smaller, focused ones.

---

## D — Dependency Inversion Principle (DIP)

High-level modules should depend on abstractions rather than concrete implementations.

This makes code more flexible and easier to test.

---

# Dependency Injection (DI)

Dependency Injection is a design pattern where an object receives its dependencies from the outside instead of creating them itself.

Without Dependency Injection:

```text
Service

↓

Creates Database Session

↓

Uses Database
```

With Dependency Injection:

```text
Database Session

↓

Injected into Service

↓

Service uses it
```

### Benefits

- Loose coupling
- Easier testing
- Better modularity
- Reusable components

FastAPI provides built-in support for Dependency Injection using the `Depends()` function.

---

# Repository Pattern

The Repository Pattern separates database logic from business logic.

Instead of writing queries inside services:

```text
Service

↓

SQL Query
```

We write:

```text
Service

↓

Repository

↓

Database
```

### Benefits

- Cleaner code
- Easier database migration
- Better testing
- Reusable queries
- Centralized database operations

Repositories act as a bridge between the application and the database.

---

# Summary

Our backend follows a layered architecture where every layer has one responsibility.

```text
Frontend
    │
    ▼
API Routes
    │
    ▼
Services
    │
    ▼
Repositories
    │
    ▼
SQLAlchemy Models
    │
    ▼
PostgreSQL
```

By combining **Clean Architecture**, **SOLID principles**, **Dependency Injection**, and the **Repository Pattern**, we create a backend that is modular, scalable, secure, and easy to maintain—qualities expected in production-grade software.