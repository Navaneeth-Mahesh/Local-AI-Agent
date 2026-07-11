# Installing PostgreSQL & Understanding the Database Server

---

# Learning Objectives

By the end of this lesson, you will understand:

- What PostgreSQL is
- What a Database Server is
- The difference between a Server and a Client
- What pgAdmin is
- What `psql` is
- How PostgreSQL stores data
- What a Database Cluster is
- What Port 5432 means
- Authentication in PostgreSQL
- Users and Roles
- Databases
- Schemas
- Why we install PostgreSQL before SQLAlchemy
- How our FastAPI application will communicate with PostgreSQL

> **Important**
>
> This lesson focuses on understanding PostgreSQL and setting it up correctly.
> We will not write any Python database code yet.

---

# Before We Start

In the previous lesson, we learned:

- What databases are
- Tables
- Rows
- Columns
- SQL
- CRUD
- PostgreSQL
- Transactions
- ACID

Now it's time to install PostgreSQL.

But before installing it, we need to understand **what we're actually installing.**

Many beginners think PostgreSQL is just another application.

It isn't.

It is actually a **Database Server**.

Understanding this concept will make SQLAlchemy and FastAPI much easier later.

---

# Imagine This...

Suppose you're building Instagram.

Every second, users are:

- Creating accounts
- Uploading photos
- Liking posts
- Sending messages
- Following users

Where is all of this data stored?

Not inside Python.

Not inside React.

Instead, a dedicated database server stores everything.

```
Users

↓

Backend (FastAPI)

↓

PostgreSQL Server

↓

Disk Storage
```

The database server is responsible for safely storing and retrieving data.

---

# What is PostgreSQL?

PostgreSQL is an **Open-Source Relational Database Management System (RDBMS).**

Let's simplify that.

PostgreSQL is software whose job is to:

- Store data
- Organize data
- Retrieve data
- Update data
- Delete data
- Protect data
- Handle thousands of users simultaneously

Think of PostgreSQL as a highly intelligent digital librarian.

You ask:

```
Give me user with ID = 5
```

PostgreSQL quickly finds it and returns the result.

---

# What Does "Database Server" Mean?

Many beginners confuse:

- Database
- Database Server

They are different.

Think about a library.

```
Library Building

↓

Contains

↓

Books
```

Similarly,

```
PostgreSQL Server

↓

Contains

↓

Databases
```

The server manages databases.

The databases contain tables.

The tables contain rows.

---

# Understanding the Hierarchy

```
PostgreSQL Server
│
├── Database
│      │
│      ├── Tables
│      │      │
│      │      ├── Rows
│      │      └── Rows
│      │
│      └── Tables
│
└── Database
```

This hierarchy is extremely important.

---

# What is a Server?

The word "Server" doesn't necessarily mean a powerful computer.

A server is simply a program that waits for requests and responds.

Earlier we learned:

```
Browser

↓

FastAPI Server

↓

Response
```

Exactly the same idea applies here.

```
FastAPI

↓

PostgreSQL Server

↓

Database Response
```

PostgreSQL continuously waits for queries.

```
SELECT

INSERT

UPDATE

DELETE
```

Whenever it receives one,

it processes it and returns the result.

---

# PostgreSQL Runs All the Time

After installation,

PostgreSQL runs as a background service.

```
Windows Starts

↓

PostgreSQL Starts

↓

Waits for Requests
```

It keeps running,

even if your FastAPI application isn't running.

This is why you can connect from many applications simultaneously.

---

# Server vs Client

One of the most important concepts.

Imagine a restaurant.

```
Customer

↓

Waiter

↓

Kitchen
```

The customer doesn't cook.

Similarly,

```
Client

↓

Server
```

The client asks.

The server performs the work.

---

## PostgreSQL Server

Responsible for:

- Storing data
- Executing SQL
- Managing users
- Managing permissions
- Handling transactions
- Managing connections

---

## PostgreSQL Client

Responsible for:

- Sending SQL commands
- Displaying results

Clients don't store data.

They simply communicate with the server.

---

# Examples of PostgreSQL Clients

There are many clients.

```
pgAdmin

psql

DBeaver

TablePlus

Your FastAPI Application
```

All of them connect to the same PostgreSQL Server.

---

# What is pgAdmin?

pgAdmin is a graphical user interface (GUI) for PostgreSQL.

Think of it as the control panel for your database.

Using pgAdmin you can:

- Create databases
- Create tables
- View records
- Execute SQL queries
- Backup databases
- Restore databases
- Manage users
- Monitor activity

Instead of typing SQL all the time,

you can use a visual interface.

---

# What is `psql`?

`psql` is PostgreSQL's command-line client.

Instead of clicking buttons,

you type commands.

Example:

```sql
SELECT * FROM users;
```

Both pgAdmin and psql connect to the same PostgreSQL Server.

The difference is only the interface.

```
pgAdmin

↓

PostgreSQL Server

↓

Database
```

```
psql

↓

PostgreSQL Server

↓

Database
```

---

# Where Does PostgreSQL Store Data?

A common misconception is that PostgreSQL stores everything inside your project folder.

It doesn't.

The data is stored in a special directory called the **Data Directory**.

```
Project

↓

Connects to

↓

PostgreSQL Server

↓

Reads Data Directory
```

Even if you delete your FastAPI project,

your database still exists.

---

# What is a Database Cluster?

During installation,

PostgreSQL creates something called a **Database Cluster**.

A cluster is simply a collection of:

- Databases
- Users
- Roles
- Configuration
- Logs

Think of it as the home for everything PostgreSQL manages.

```
Cluster
│
├── Database A
├── Database B
├── Users
├── Roles
└── Settings
```

For now,

just remember:

> One PostgreSQL installation creates one database cluster.

---

# Understanding Port 5432

Every server listens on a network port.

FastAPI usually listens on:

```
8000
```

React development server:

```
5173
```

PostgreSQL listens on:

```
5432
```

This means whenever an application wants to talk to PostgreSQL,

it connects to:

```
localhost:5432
```

Think of a port as a door.

Different applications use different doors.

```
FastAPI

Door 8000
```

```
React

Door 5173
```

```
PostgreSQL

Door 5432
```

---

# Authentication in PostgreSQL

Not everyone should access your database.

PostgreSQL requires users to authenticate.

Every connection needs:

- Username
- Password
- Database Name

Example:

```
Host

localhost

↓

Port

5432

↓

Username

postgres

↓

Password

********

↓

Database

ai_agent
```

Only after successful authentication does PostgreSQL allow access.

---

# Users and Roles

In PostgreSQL,

users are managed through **Roles**.

A role can:

- Create databases
- Read tables
- Insert data
- Delete data
- Manage permissions

For now,

we'll use the default administrator role:

```
postgres
```

Later,

in production,

applications usually have their own limited database user.

---

# Creating Our First Database

During installation,

PostgreSQL creates the server,

but not our application database.

We'll create one called:

```
ai_agent
```

This database will contain:

```
Users

Conversations

Messages

Memories

Documents

Settings

API Keys

Plugins
```

Everything related to our AI Agent will live inside this database.

---

# How FastAPI Will Connect

Soon,

our architecture will look like this:

```
React Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
SQLAlchemy
        │
        ▼
PostgreSQL Server
        │
        ▼
Database
```

Notice something important.

FastAPI never talks directly to database files.

It communicates with the PostgreSQL Server.

The server handles everything else.

---

# Installing PostgreSQL (Windows)

1. Download PostgreSQL from the official website.
2. Run the installer.
3. Select the following components:
   - PostgreSQL Server
   - pgAdmin 4
   - Command Line Tools
4. Choose an installation directory.
5. Set a password for the `postgres` user.
6. Leave the default port as **5432**.
7. Complete the installation.

---

# Verify the Installation

Open **pgAdmin**.

You should see a server similar to:

```
Servers
└── PostgreSQL 17
```

Expand it.

You should be able to browse:

- Databases
- Login Roles
- Tablespaces

This confirms your PostgreSQL Server is running correctly.

---

# Key Takeaways

After this lesson, you should understand:

- PostgreSQL is a Database Management System (RDBMS).
- A Database Server manages one or more databases.
- A Server is different from a Client.
- pgAdmin and `psql` are PostgreSQL clients.
- PostgreSQL stores data in its own data directory.
- PostgreSQL listens on port **5432**.
- Authentication requires a username, password, and database.
- Users are managed through Roles.
- FastAPI communicates with the PostgreSQL Server, not directly with database files.

---

# What's Next?

In the next lesson, we'll connect our FastAPI application to PostgreSQL.

You'll learn:

- What SQLAlchemy is
- What an ORM is
- Why ORMs exist
- What a Database Engine is
- What Sessions are
- What Connection Pooling is
- How FastAPI communicates with PostgreSQL using SQLAlchemy

By the end of the next lesson, you'll understand the complete journey from a Python object to a row stored inside your PostgreSQL database.