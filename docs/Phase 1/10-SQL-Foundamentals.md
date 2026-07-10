# SQL Fundamentals

## Goal

By the end of this lesson, you'll:

* Understand what SQL is
* Write your first SQL queries
* Learn CRUD using SQL
* Understand constraints
* Understand how SQLAlchemy works internally
* Be ready to learn SQLAlchemy in Lesson 8

---

# First Question

You already know Python.

Python understands:

```python
print("Hello")
```

JavaScript understands:

```javascript
console.log("Hello")
```

So...

**What language does PostgreSQL understand?**

Answer:

**SQL**

---

# What is SQL?

SQL stands for:

> **Structured Query Language**

It is the language used to communicate with relational databases.

Think of it like this:

```
Python

↓

FastAPI

↓

SQL

↓

PostgreSQL
```

Your Python code **doesn't directly manipulate the database**.

Eventually, SQL commands reach PostgreSQL.

---

# What Does SQL Do?

SQL lets us:

* Create tables
* Insert data
* Read data
* Update data
* Delete data

That's all databases really do.

---

# CRUD

Every backend application performs these four operations.

## Create

Example:

```
Register User
```

Database action:

```
INSERT
```

---

## Read

Example:

```
Login User
```

Database action:

```
SELECT
```

---

## Update

Example:

```
Change Password
```

Database action:

```
UPDATE
```

---

## Delete

Example:

```
Delete Account
```

Database action:

```
DELETE
```

Everything you build in backend engineering comes back to these four operations.

---

# Creating a Table

Imagine we want to store users.

We need a table.

SQL:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255),
    password_hash TEXT
);
```

Let's understand every line.

---

## CREATE TABLE

```sql
CREATE TABLE users
```

Means:

> Create a table named `users`.

---

## Column Definitions

```sql
id SERIAL PRIMARY KEY
```

### SERIAL

Automatically generates:

```
1

2

3

4
```

No need to manually assign IDs.

---

### PRIMARY KEY

Every user must have a unique ID.

Never duplicated.

---

Next column:

```sql
username VARCHAR(100)
```

Means:

```
Text

Maximum length = 100
```

---

Email

```sql
email VARCHAR(255)
```

Maximum 255 characters.

---

Password

```sql
password_hash TEXT
```

We use `TEXT` because hashed passwords can be long.

---

# Data Types

Common PostgreSQL data types you'll use:

| Type         | Purpose           | Example      |
| ------------ | ----------------- | ------------ |
| INTEGER      | Whole numbers     | 25           |
| SERIAL       | Auto-increment ID | 1, 2, 3      |
| VARCHAR(100) | Short text        | Name         |
| TEXT         | Long text         | AI responses |
| BOOLEAN      | True/False        | is_admin     |
| TIMESTAMP    | Date & Time       | Login time   |

We'll use these throughout the project.

---

# Inserting Data

Now let's create a user.

```sql
INSERT INTO users (
    username,
    email,
    password_hash
)
VALUES (
    'Navaneeth',
    'nav@gmail.com',
    'hashed_password'
);
```

Read it like English:

> Insert into users these columns with these values.

---

# Reading Data

Show every user.

```sql
SELECT * FROM users;
```

Meaning:

```
SELECT

↓

Everything

↓

FROM users
```

---

# Reading Specific Columns

Instead of everything:

```sql
SELECT username, email
FROM users;
```

Returns only those columns.

---

# Filtering Data

Suppose you want only one user.

```sql
SELECT *
FROM users
WHERE id = 1;
```

Meaning:

```
Give me

↓

Only rows

↓

Where ID equals 1
```

---

Another example:

```sql
SELECT *
FROM users
WHERE email = 'nav@gmail.com';
```

This is exactly what happens during login.

---

# Updating Data

User changes email.

```sql
UPDATE users
SET email = 'new@gmail.com'
WHERE id = 1;
```

Always notice the `WHERE`.

Without it:

```sql
UPDATE users
SET email = 'abc@gmail.com';
```

Every user's email becomes:

```
abc@gmail.com
```

One missing `WHERE` can update every row in the table.

---

# Deleting Data

Delete one user.

```sql
DELETE FROM users
WHERE id = 1;
```

Again,

Never forget the `WHERE`.

Otherwise:

```sql
DELETE FROM users;
```

Every user disappears.

---

# Constraints

A database should protect itself.

Suppose two users register with the same email.

Should that be allowed?

No.

So we add:

```sql
email VARCHAR(255) UNIQUE
```

Now PostgreSQL guarantees no duplicate emails.

Even if your backend has a bug, the database enforces the rule.

---

# NOT NULL

Suppose username is required.

```sql
username VARCHAR(100) NOT NULL
```

Now PostgreSQL refuses:

```sql
INSERT INTO users (...);
```

if `username` is missing.

The database helps maintain data integrity.

---

# Default Values

Suppose every new user should be active by default.

```sql
is_active BOOLEAN DEFAULT TRUE
```

Now every new row gets:

```
TRUE
```

unless specified otherwise.

---

# How SQL Fits Into Our AI Agent

When a user registers:

```
Frontend

↓

FastAPI

↓

Service

↓

Repository

↓

SQL

↓

PostgreSQL
```

Even though we'll write Python using SQLAlchemy later, SQL is still the language executed underneath.

---

# Why Learn SQL if We're Using SQLAlchemy?

This is one of the biggest mistakes beginners make.

They jump straight into SQLAlchemy without understanding SQL.

Then they see:

```python
session.query(User).filter(...)
```

and have no idea what's happening.

In reality, SQLAlchemy generates SQL behind the scenes.

Understanding SQL helps you:

* Debug queries
* Optimize performance
* Read database logs
* Write better applications

---

# SQL vs SQLAlchemy

Raw SQL:

```sql
SELECT *
FROM users
WHERE id = 1;
```

SQLAlchemy (we'll learn this next):

```python
session.query(User).filter(User.id == 1).first()
```

Same result.

Different syntax.

---

# SQL Execution Order

When FastAPI receives:

```
POST /login
```

Internally:

```
FastAPI

↓

Repository

↓

SQLAlchemy

↓

SQL

↓

PostgreSQL

↓

Result

↓

Python Object

↓

JSON Response
```

SQLAlchemy acts as a translator between Python and SQL.

---

# Summary

Today you learned:

* What SQL is
* Why databases use SQL
* CRUD operations
* `CREATE TABLE`
* `INSERT`
* `SELECT`
* `UPDATE`
* `DELETE`
* `WHERE`
* Data types
* Constraints (`PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `DEFAULT`)
* Why learning SQL is important even when using an ORM

---

# Mini Challenge

Without looking back, answer these questions:

1. What does `SELECT * FROM users;` do?
2. Why is `WHERE` important in `UPDATE` and `DELETE` statements?
3. What is the purpose of a `PRIMARY KEY`?
4. Why should `email` usually have a `UNIQUE` constraint?
5. What's the difference between `VARCHAR(100)` and `TEXT`?
6. Why are we learning SQL before SQLAlchemy?

If you can answer those confidently, you've understood SQL fundamentals.

---


