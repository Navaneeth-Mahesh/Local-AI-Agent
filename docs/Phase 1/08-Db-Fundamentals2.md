# (Part 2)
# SQL, CRUD, ACID & Why We Chose PostgreSQL

---

# Learning Objectives

By the end of this lesson, you will understand:

- What SQL is
- The four CRUD operations
- The difference between SQL and NoSQL databases
- Why we're choosing PostgreSQL
- What ACID properties are
- What database transactions are
- How our AI Agent's database will be designed

---

# Introduction

In the previous lesson, we learned that databases store and organize data using:

- Tables
- Rows
- Columns
- Primary Keys
- Foreign Keys
- Relationships

Now it's time to understand **how we communicate with a database** and **why PostgreSQL is the best choice for our AI Agent**.

Unlike Python, JavaScript, or Java, databases don't understand programming languages.

They understand one language:

> **SQL**

---

# What is SQL?

SQL stands for:

> **Structured Query Language**

It is the standard language used to communicate with relational databases.

Think of SQL as the language that databases speak.

Whenever your application wants to:

- Create data
- Read data
- Update data
- Delete data

it sends SQL commands to the database.

---

# Real-World Analogy

Imagine you're in a library.

You don't walk into the storage room and search every shelf yourself.

Instead, you ask the librarian:

> "Please find the book titled Python Basics."

The librarian understands your request and brings you the correct book.

SQL works the same way.

Your application asks:

```
Find user with ID = 1
```

The database searches through millions of records and returns the correct result.

---

# Basic SQL Operations

Suppose we have a table called:

```
Users
```

```
+----+----------------------+----------------+
| id | email                | password_hash  |
+----+----------------------+----------------+
| 1  | nav@gmail.com        | ******         |
| 2  | john@gmail.com       | ******         |
+----+----------------------+----------------+
```

Now let's see how SQL communicates with this table.

---

# SELECT

Suppose we want every user.

SQL:

```sql
SELECT * FROM users;
```

Meaning:

> Return every row from the `users` table.

---

Suppose we only want one user.

```sql
SELECT * FROM users
WHERE id = 1;
```

Meaning:

> Find the user whose ID is 1.

---

# INSERT

When a new user registers,

the application needs to add a new row.

SQL:

```sql
INSERT INTO users (email, password_hash)
VALUES ('nav@gmail.com', 'hashed_password');
```

Meaning:

> Create a new user.

---

# UPDATE

Suppose the user changes their password.

SQL:

```sql
UPDATE users
SET password_hash = 'new_hash'
WHERE id = 1;
```

Meaning:

> Update the password for user ID 1.

---

# DELETE

Suppose the user deletes their account.

SQL:

```sql
DELETE FROM users
WHERE id = 1;
```

Meaning:

> Remove this user from the database.

---

# CRUD Operations

Almost every backend application performs only four types of database operations.

These are known as **CRUD**.

| Operation | Meaning | Example |
|-----------|---------|---------|
| Create | Add new data | Register User |
| Read | Retrieve data | Login User |
| Update | Modify existing data | Change Password |
| Delete | Remove data | Delete Account |

You'll hear the term CRUD throughout your backend journey.

Whether you're building:

- Banking software
- Social media
- AI applications
- E-commerce platforms

everything revolves around CRUD.

---

# SQL vs NoSQL

Modern databases are generally divided into two categories.

```
Databases

├── SQL
└── NoSQL
```

Let's compare them.

---

# SQL Databases

Examples:

- PostgreSQL
- MySQL
- SQLite
- Microsoft SQL Server

These databases store data inside **tables**.

Example:

```
Users

↓

Conversations

↓

Messages

↓

Documents
```

Every table has a defined structure.

Relationships between tables are very strong.

---

# Advantages of SQL Databases

SQL databases provide:

- Strong consistency
- Relationships between tables
- Reliable transactions
- Structured data
- Powerful queries
- Excellent data integrity

This makes them perfect for applications where data accuracy is important.

---

# NoSQL Databases

Examples:

- MongoDB
- Redis
- Cassandra
- CouchDB

Instead of storing data in tables,

many NoSQL databases store JSON-like documents.

Example:

```json
{
    "name": "Navaneeth",
    "email": "nav@gmail.com",
    "messages": [
        {
            "text": "Hello AI"
        }
    ]
}
```

The structure is much more flexible.

---

# Advantages of NoSQL

NoSQL databases are useful when:

- Data changes frequently
- Relationships are minimal
- Huge scalability is required
- Flexible document structures are preferred

Different problems require different database solutions.

---

# SQL vs NoSQL Comparison

| SQL | NoSQL |
|------|--------|
| Stores data in tables | Stores data as documents, key-value pairs, graphs, or columns |
| Strong relationships | Flexible structure |
| Fixed schema | Dynamic schema |
| Excellent consistency | High flexibility |
| Great for structured data | Great for rapidly changing data |

Neither is "better."

Each solves different problems.

---

# Why We're Choosing PostgreSQL

This project isn't a simple chatbot.

Our AI Agent will manage:

- User accounts
- Authentication
- Conversations
- Messages
- Memories
- Permissions
- Documents
- Plugins
- API Keys
- User Settings

Notice something.

Almost everything is connected.

Example:

```
User

↓

Conversation

↓

Messages

↓

Memory

↓

Documents
```

These relationships are exactly what relational databases are designed for.

---

# PostgreSQL and AI

One of PostgreSQL's biggest strengths is its ecosystem.

Later in this project,

we'll use an extension called:

```
pgvector
```

This allows PostgreSQL to store:

- Traditional relational data
- AI vector embeddings

inside the same database.

That means one database can power:

- Authentication
- Chat History
- Long-Term Memory
- Semantic Search

This is one of the reasons PostgreSQL has become extremely popular in AI applications.

---

# ACID Properties

One reason PostgreSQL is trusted worldwide is that it follows the **ACID** principles.

ACID ensures that your data remains correct and reliable, even if something goes wrong.

Let's understand each principle.

---

# A — Atomicity

Atomicity means:

> A transaction either completes entirely or not at all.

Imagine transferring ₹1000 from one bank account to another.

```
Account A

↓

₹1000 removed

↓

Account B

↓

₹1000 added
```

Both steps must happen together.

Suppose money leaves Account A,

but never reaches Account B.

That would be disastrous.

Instead,

the database ensures:

```
Success

OR

Rollback Everything
```

Nothing happens halfway.

---

# C — Consistency

Consistency means:

> The database always remains in a valid state.

Suppose a message references a user.

```
Message

↓

User ID = 5
```

If User 5 doesn't exist,

the database rejects the operation.

It protects the integrity of your data.

---

# I — Isolation

Imagine two users register at exactly the same time.

```
User A

↓

Register

```

At the same moment:

```
User B

↓

Register
```

The database ensures these operations don't interfere with one another.

Each transaction behaves as though it is running independently.

---

# D — Durability

Durability means:

> Once data is successfully saved, it stays saved.

Imagine a user sends an important message to the AI.

The database confirms:

```
Message Saved
```

Immediately afterward,

the server loses power.

When the server starts again,

the conversation is still there.

The data survives crashes and restarts.

---

# What is a Transaction?

A transaction is a group of database operations treated as a single unit of work.

Either:

```
Everything succeeds
```

or

```
Everything fails
```

There is no middle ground.

---

# Example

Imagine user registration.

The application performs:

```
Create User

↓

Create User Settings

↓

Create Default Conversation

↓

Create Default Memory
```

Suppose:

```
User Created ✅

Settings Created ✅

Conversation Failed ❌
```

Without transactions,

the database would contain incomplete information.

Instead,

the database rolls everything back.

```
Nothing Saved
```

The system stays consistent.

---

# Why Transactions Matter

Transactions protect us from:

- Partial updates
- Corrupted data
- System crashes
- Unexpected failures

Professional applications rely heavily on transactions.

---

# Database Design for Our AI Agent

Over the next several lessons,

we'll gradually build the following database.

```
Users
│
├── id
├── username
├── email
├── password_hash
└── created_at
```

↓

```
Conversations
│
├── id
├── user_id
├── title
└── created_at
```

↓

```
Messages
│
├── id
├── conversation_id
├── role
├── content
└── created_at
```

↓

```
Memories
│
├── id
├── user_id
├── text
├── importance
└── embedding
```

↓

```
Documents
│
├── id
├── user_id
├── filename
├── path
└── uploaded_at
```

Each table has a specific responsibility.

Together,

they create the complete data model for our AI Agent.

---

# How Everything Connects

By the end of this project,

our data flow will look like this:

```
React Frontend

↓

FastAPI

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy ORM

↓

PostgreSQL Database
```

Notice something important.

FastAPI doesn't communicate directly with PostgreSQL.

Instead,

SQLAlchemy acts as a bridge between Python and the database.

We'll learn about SQLAlchemy in the next lessons.

---

# Key Takeaways

After this lesson, you should understand:

- SQL is the language used to communicate with relational databases.
- CRUD represents the four basic database operations.
- SQL databases organize data into tables with relationships.
- NoSQL databases provide flexible document-based storage.
- PostgreSQL is an excellent choice because it supports strong relationships, transactions, and AI extensions like `pgvector`.
- ACID properties ensure data remains accurate and reliable.
- Transactions prevent partial updates and maintain consistency.
- Our AI Agent's database will grow into a connected system of tables representing users, conversations, messages, memories, and documents.

---

# What's Next?

In the next lesson, we'll move from database concepts to the PostgreSQL ecosystem.

You'll learn:

- What PostgreSQL actually is
- PostgreSQL Server vs Client
- What a Database Server does
- What `psql` is
- What pgAdmin is
- Database users and roles
- Ports and connections
- How our FastAPI application will connect to PostgreSQL

Once you understand these concepts, we'll be ready to connect our backend to a real PostgreSQL database using SQLAlchemy.