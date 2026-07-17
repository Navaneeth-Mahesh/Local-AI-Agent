# Repository Pattern, Service Layer & Building the User Module

---

# Learning Objectives

By the end of this lesson, you will understand:

* Why professional applications are divided into layers
* What Clean Architecture is
* What the Repository Pattern is
* What the Service Layer does
* What API Routes are responsible for
* How Schemas, Services, and Repositories work together
* How a request travels through the backend
* Why separating responsibilities makes applications easier to maintain

---

# Before We Start

Imagine a user clicks the **Register** button.

They enter:

```text
Username: Navaneeth

Email: nav@gmail.com

Password: MyPassword123
```

The frontend sends this request to our backend.

Now ask yourself:

> **Where should the registration logic be written?**

Many beginners put everything inside a single API route.

Example:

```python
@app.post("/register")
def register():
    # Validate input
    # Check duplicate email
    # Hash password
    # Create database object
    # Save to database
    # Generate response
```

For a small project, this works.

But imagine your application grows to:

* 50 API endpoints
* 100 database models
* 20,000+ lines of code

Now every route becomes hundreds of lines long.

Finding bugs becomes difficult.

Testing becomes difficult.

Reusing code becomes difficult.

Professional software avoids this problem by separating responsibilities into different layers.

---

# Why Layered Architecture?

Instead of placing all the code in one function, we divide the application into multiple layers.

Each layer has **one responsibility**.

```
Frontend

↓

API Routes

↓

Services

↓

Repositories

↓

Database
```

Every layer performs one task and passes the work to the next layer.

This makes the project:

* Easier to understand
* Easier to test
* Easier to maintain
* Easier to scale

---

# Imagine Building a House

Think of building a house.

Would one person do everything?

```
Architect

↓

Engineer

↓

Electrician

↓

Plumber

↓

Painter
```

No.

Each person specializes in one task.

Backend architecture follows the same idea.

Each layer specializes in one responsibility.

---

# The Four Main Layers

## 1. API Layer

The API Layer is the entry point of the application.

Every request from the frontend arrives here first.

Responsibilities:

* Receive HTTP requests
* Validate incoming data
* Call the appropriate Service
* Return an HTTP response

The API Layer **should not**:

* Query the database
* Hash passwords
* Generate JWT tokens
* Contain business logic

Think of it as a receptionist.

It receives the request and forwards it to the correct department.

---

## Example

```
POST /auth/register
```

↓

API Route

↓

AuthService.register()

The API Route doesn't know **how** registration works.

It only knows **who should handle it**.

---

# 2. Service Layer

The Service Layer is the **brain** of the application.

This is where business rules live.

When a user registers, the service decides:

```
Is the email already used?

↓

Is the password valid?

↓

Hash the password

↓

Create the user

↓

Return the result
```

Notice something important.

The Service knows **what should happen**, but not **how the database stores data**.

---

## Responsibilities

Services contain:

* Business rules
* Authentication logic
* Authorization
* Password hashing
* AI integration
* Permission checks
* Workflow coordination

Services should not contain SQL queries.

---

# 3. Repository Layer

Repositories are responsible for talking to the database.

Instead of writing SQL inside Services, we place every database operation inside repositories.

Think of the Repository as the translator between Python and PostgreSQL.

```
Service

↓

Repository

↓

Database
```

The Service simply says:

> "Find this user."

The Repository knows **how** to perform that operation.

---

## Responsibilities

Repositories:

* Create records
* Read records
* Update records
* Delete records

Also known as **CRUD operations**.

---

## Example

```
Find User

↓

Repository searches database

↓

Returns User
```

The Service doesn't care whether the data comes from PostgreSQL, MySQL, or MongoDB.

It simply receives a User object.

---

# Why Is This Important?

Imagine we switch from PostgreSQL to MySQL tomorrow.

Should the API change?

No.

Should the Service change?

No.

Only the Repository changes.

That's one of the biggest advantages of this architecture.

---

# 4. Database Layer

The Database stores information permanently.

Examples:

* Users
* Conversations
* Messages
* AI memory
* Settings
* Refresh tokens

The database doesn't know anything about HTTP, JWT, or FastAPI.

It simply stores data.

---

# Complete Registration Flow

Let's follow one request from beginning to end.

```
Frontend

↓

POST /auth/register

↓

API Route

↓

UserRegister Schema validates request

↓

Auth Service

↓

User Repository

↓

PostgreSQL

↓

Repository returns User

↓

Auth Service

↓

UserResponse Schema

↓

JSON Response

↓

Frontend
```

This is exactly how almost every feature in our AI Agent will work.

---

# Understanding Each Folder

```
app/

├── api/
├── services/
├── repositories/
├── schemas/
├── models/
└── database/
```

Each folder exists for a reason.

---

## api/

Contains API endpoints.

Examples:

```
POST /login

POST /register

GET /users/me
```

Routes should stay small.

---

## services/

Contains business logic.

Examples:

* Register user
* Login user
* Generate JWT
* Verify permissions

---

## repositories/

Contains database operations.

Examples:

* Create user
* Find user
* Update user
* Delete user

---

## schemas/

Defines request and response structures.

Examples:

```
UserRegister

UserLogin

UserResponse

Token
```

Schemas validate data entering and leaving the application.

---

## models/

Defines SQLAlchemy models.

Each model represents one database table.

Examples:

```
User

Conversation

Message
```

---

## database/

Contains:

* Database connection
* Session management
* Database configuration

---

# Separation of Concerns

One of the most important software engineering principles is **Separation of Concerns**.

It means:

> Every part of the application should focus on one specific job.

Instead of one file doing everything,

```
Route

↓

Validation

↓

Password Hashing

↓

SQL Query

↓

JWT

↓

Response
```

we divide responsibilities:

```
Route

↓

Service

↓

Repository

↓

Database
```

Each layer becomes smaller, cleaner, and easier to understand.

---

# Error Handling

Suppose a user tries to register using an email that already exists.

Who should detect this?

The Repository.

Who should decide what to do?

The Service.

Who should return an HTTP error?

The API Route.

Example flow:

```
Repository

↓

User already exists

↓

Service

↓

Raises EmailAlreadyExists

↓

API Route

↓

Returns

409 Conflict
```

Each layer performs only its own responsibility.

---

# Dependency Injection

Notice that the Repository doesn't create a database session.

Instead, FastAPI provides it.

```
FastAPI

↓

Depends(get_db)

↓

Database Session

↓

Repository

↓

Service

↓

Route
```

This is called **Dependency Injection**.

It makes the application easier to test and reuse.

---

# Common Beginner Mistakes

❌ Writing SQL inside API Routes

Routes should only receive requests and return responses.

---

❌ Hashing passwords inside Repositories

Password hashing is business logic.

It belongs in the Service Layer.

---

❌ Generating JWT tokens inside Repositories

Repositories should only communicate with the database.

Authentication belongs to the Service Layer.

---

❌ Returning SQLAlchemy models directly

Always return Response Schemas.

This prevents leaking sensitive data such as password hashes.

---

❌ Putting everything inside `main.py`

Large applications should be organized into modules based on responsibility.

---

# Key Takeaways

After this lesson, you should understand:

* Why professional applications use layered architecture.
* The responsibility of API Routes, Services, Repositories, and the Database.
* How Schemas validate requests and responses.
* Why Separation of Concerns leads to cleaner, more maintainable code.
* How Dependency Injection reduces coupling between components.
* How a single request flows through the backend from the frontend to the database and back.

---
