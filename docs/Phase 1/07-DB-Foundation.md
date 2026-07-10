# Phase 1 — Lesson 5: Database Fundamentals

> **Goal:** By the end of this lesson, you'll understand **how databases work**, **why we need them**, and **why PostgreSQL is the right choice** for our AI Agent.

**Important:** We will **not** write any code in this lesson.

First, we understand the concepts. Then we build.

---

# Imagine We Don't Have a Database

Our AI Agent has:

* User Registration
* Login
* Chat History
* Memories
* Settings
* API Keys

Where should we store all of this?

Option 1:

```python
users = []
```

Problem?

When you stop the application:

```text
users = []

↓

Application closes

↓

Everything disappears
```

Not useful.

---

Option 2

Store everything in a text file.

```text
users.txt

Navaneeth
password123
```

Problems:

* Slow
* Hard to search
* Hard to update
* Unsafe
* Not scalable

---

So we need something better.

That is a **Database**.

---

# What is a Database?

A database is:

> **A system that stores, organizes, retrieves, updates, and deletes data efficiently.**

Think of a huge digital library.

Instead of books,

it stores data.

---

# Real World Analogy

Imagine your college.

They have information about:

* Students
* Teachers
* Courses
* Attendance
* Marks

Could they store everything in one Excel sheet?

No.

Instead,

they use a database.

---

# What Data Will Our AI Agent Store?

Quite a lot.

```text
Users

↓

Conversations

↓

Messages

↓

Memories

↓

Documents

↓

Permissions

↓

API Keys

↓

Settings

↓

Plugins
```

Everything lives inside PostgreSQL.

---

# How Does a Database Organize Data?

Imagine Excel.

| ID | Name      | Age |
| -- | --------- | --- |
| 1  | Navaneeth | 19  |
| 2  | John      | 22  |

This looks familiar.

A relational database works similarly.

Instead of calling it an Excel sheet,

we call it a **Table**.

---

# Table

Example:

```text
Users
```

| id | email | password |
| -- | ----- | -------- |

The whole thing is called a **Table**.

---

# Row

Each user is one row.

| id | email                                 |
| -- | ------------------------------------- |
| 1  | [abc@gmail.com](mailto:abc@gmail.com) |

One horizontal entry.

---

# Column

Columns describe the properties.

```text
id

email

password

created_at
```

Every user has these columns.

---

# Visual Representation

```text
Users Table

+----+----------------------+----------------+
| id | email                | password_hash  |
+----+----------------------+----------------+
| 1  | nav@gmail.com        | ******         |
| 2  | john@gmail.com       | ******         |
+----+----------------------+----------------+
```

---

# Primary Key

Every table needs a way to uniquely identify each row.

Example

```
Navaneeth
```

Could there be another Navaneeth?

Yes.

Names aren't unique.

Instead

```
ID = 1
```

Only one row can have ID = 1.

That is called the **Primary Key**.

---

Properties:

* Unique
* Never duplicated
* Usually never changes

Example

```text
Users

ID

1

2

3

4
```

---

# Foreign Key

Now imagine another table.

Messages

| id | user_id | message |
| -- | ------- | ------- |

Question:

How do we know who sent the message?

Answer:

```
user_id
```

Suppose

Users

| id | name      |
| -- | --------- |
| 1  | Navaneeth |

Messages

| id | user_id | message  |
| -- | ------- | -------- |
| 5  | 1       | Hello AI |

The number **1** points to the user.

This is called a **Foreign Key**.

It creates relationships between tables.

---

# Relationships

Databases are relational because tables relate to one another.

Example:

One User

↓

Many Conversations

```
User

↓

Conversation

Conversation

Conversation
```

This is called

> **One-to-Many**

---

Another example.

Conversation

↓

Many Messages

```
Conversation

↓

Message

Message

Message
```

Again,

One-to-Many.

---

# Our Database Relationships

```text
User

↓

Conversations

↓

Messages

↓

Memories

↓

Documents
```

Everything connects together.

---

# SQL

Databases understand SQL.

SQL means

**Structured Query Language**

It is the language databases speak.

Example:

```sql
SELECT * FROM users;
```

Means

> Give me every user.

Another:

```sql
SELECT * FROM users
WHERE id = 1;
```

Means

Give me the user whose ID is 1.

---

# CRUD

Every backend application performs only four main database operations.

Create

```text
Register User
```

Read

```text
Login User
```

Update

```text
Change Password
```

Delete

```text
Delete Account
```

Together these are called **CRUD**.

You'll hear this term constantly.

---

# SQL vs NoSQL

There are two major categories.

---

## SQL Databases

Examples

* PostgreSQL
* MySQL
* SQLite

Data is stored in tables.

Example

```text
Users

↓

Messages

↓

Documents
```

Relationships are very strong.

---

## NoSQL Databases

Examples

* MongoDB
* Redis
* Cassandra

Instead of tables,

they often store JSON-like documents.

Example

```json
{
  "name": "Navaneeth",
  "messages": [
    {
      "text": "Hello"
    }
  ]
}
```

More flexible,

but different trade-offs.

---

# Why Are We Choosing PostgreSQL?

Many people ask:

> Why not MongoDB?

Our project has:

* Users
* Conversations
* Permissions
* Roles
* API Keys
* Memories
* Documents
* Plugins

These all have relationships.

PostgreSQL handles relationships exceptionally well.

Later,

it also supports

```text
pgvector
```

which lets us perform AI semantic search.

That means one database can store both:

* relational data
* vector embeddings

Perfect for AI applications.

---

# ACID Properties

One reason PostgreSQL is trusted is that it follows the **ACID** principles.

---

## A — Atomicity

Think of a bank transfer.

You send ₹1000.

Money should:

* leave Account A
* reach Account B

Both happen.

Or neither happens.

Never half.

---

## C — Consistency

The database always remains valid.

Example:

A message cannot belong to a user who doesn't exist.

Rules are enforced automatically.

---

## I — Isolation

Imagine two users register at the exact same moment.

Their operations shouldn't interfere with each other.

The database handles concurrent operations safely.

---

## D — Durability

Once data is committed,

it survives power failures or application crashes.

If your AI Agent stores a conversation,

it won't disappear because the server restarted.

---

# Transactions

Imagine registration.

Steps:

```text
Create User

↓

Create Settings

↓

Create Default Conversation
```

Suppose

User is created.

Settings fail.

Now the database is inconsistent.

Instead

everything happens inside a **Transaction**.

Either:

```
All succeed
```

or

```
Everything rolls back.
```

Nothing is partially saved.

---

# Why Does Our AI Agent Need a Database?

Without a database:

Every restart loses:

* Accounts
* Chat history
* Memories
* Documents
* Settings
* API keys

With PostgreSQL:

Everything is safely stored and can be retrieved whenever the user logs in.

---

# Database Design for Our AI Agent

Over the next few lessons, we'll build tables like this:

```text
Users
│
├── id
├── username
├── email
├── password_hash
└── created_at
```

```text
Conversations
│
├── id
├── user_id
├── title
└── created_at
```

```text
Messages
│
├── id
├── conversation_id
├── role
├── content
└── timestamp
```

```text
Memories
│
├── id
├── user_id
├── text
├── importance
└── embedding (later)
```

We'll add more tables as new features are introduced.

---

# What You Learned Today

You now understand:

* What a database is
* Why applications need databases
* Tables
* Rows
* Columns
* Primary Keys
* Foreign Keys
* Relationships
* SQL
* CRUD
* SQL vs NoSQL
* Why we're choosing PostgreSQL
* ACID properties
* Transactions
* How our AI Agent's data will be organized

---

# Mini Challenge

Before Lesson 6, answer these questions yourself:

1. Why is a text file a poor choice for storing user accounts?
2. What is the difference between a **row** and a **column**?
3. Why do we use a **Primary Key**?
4. What is a **Foreign Key**, and how does it create relationships?
5. Why is PostgreSQL a better fit for our AI Agent than storing everything in Python lists?
6. What does **CRUD** stand for?
7. If user registration creates three records and the second operation fails, why are **transactions** important?

If you can answer those confidently, you've understood the foundation.

---

## Next Lesson — Lesson 6: Installing PostgreSQL & Understanding the Database Server

We'll move from theory to practice and learn:

* What PostgreSQL actually is
* PostgreSQL Server vs Client
* What `psql` is
* What pgAdmin is
* Installing PostgreSQL on Windows
* Creating a database
* Creating a database user
* Ports (5432)
* Authentication
* Connecting to the database

After that, we'll start connecting our FastAPI backend to PostgreSQL using SQLAlchemy.
