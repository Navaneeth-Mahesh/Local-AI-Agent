Excellent. This lesson is arguably the **most important security lesson** in the entire backend course.

Almost every web application has user authentication. If you implement it incorrectly, you can expose every user's account.

Today you'll learn not just *how* to hash passwords, but *why* password hashing exists and how professional systems protect user credentials.

---

# Phase 1 — Lesson 12: Password Security & Hashing

## Goal

By the end of this lesson, you'll understand:

* Why passwords are never stored in plain text
* Hashing vs Encryption
* One-way functions
* Salting
* Password verification
* Why Argon2 is recommended
* How password hashing fits into authentication
* Implementing `security.py`

---

# Imagine This Scenario

A user registers with:

```text
Username: Navaneeth
Password: MyPassword123
```

How should we store it?

Some beginners think:

```text
users

id | username | password
-------------------------
1  | Navaneeth | MyPassword123
```

This is **one of the worst mistakes** you can make.

---

# What Happens If the Database is Leaked?

Suppose an attacker steals your database.

They immediately see:

```text
MyPassword123
```

Now they can:

* Log into your website
* Try the same password on Gmail
* Try it on Instagram
* Try it on GitHub

Many users reuse passwords.

A single database leak can compromise multiple accounts.

---

# Never Store Plain Text Passwords

Instead, store:

```text
users

id | username | password_hash
--------------------------------------------
1  | Navaneeth | $argon2id$v=19$m=65536...
```

Notice:

The original password is **gone**.

Only its hash remains.

---

# What is Hashing?

Hashing is a mathematical function.

Input:

```text
MyPassword123
```

↓

Hash Function

↓

Output:

```text
A8F72D8C913AFB...
```

The important property is:

You **cannot reverse it**.

---

# Hashing is One-Way

Think of it like this.

Egg:

```text
🥚
```

↓

Cook it

↓

```text
🍳
```

Can you turn the cooked egg back into a raw egg?

No.

Hashing is similar.

---

# Hashing vs Encryption

Many beginners confuse these.

## Encryption

```text
Message

↓

Encrypt

↓

Ciphertext

↓

Decrypt

↓

Original Message
```

Encryption is reversible.

---

## Hashing

```text
Password

↓

Hash

↓

Hash Value
```

No decryption exists.

You cannot recover the original password.

---

# Then How Does Login Work?

Good question.

Suppose the database stores:

```text
argon2_hash
```

User logs in.

They type:

```text
MyPassword123
```

The server hashes **the password they entered**.

```text
Input Password

↓

Hash

↓

Compare

↓

Stored Hash
```

If both hashes match,

the password is correct.

Notice:

The server never needs the original password.

---

# Why Can't We Compare Plain Text?

Because we intentionally never stored it.

Only the hash exists.

---

# What is Salting?

Imagine two users.

Both choose:

```text
password123
```

Without salt:

```text
User A

↓

ABCD1234
```

```text
User B

↓

ABCD1234
```

Same password.

Same hash.

An attacker immediately knows both users chose the same password.

---

# Salt Solves This

Each password gets random data added before hashing.

Example:

User A

```text
password123

+

X91L2
```

↓

Hash A

---

User B

```text
password123

+

T7KP8
```

↓

Hash B

Different hashes.

Even though the passwords are identical.

Modern algorithms like **Argon2** generate and store the salt automatically.

---

# Rainbow Table Attacks

Years ago, attackers created huge lookup tables.

Example:

```text
password123

↓

Known Hash
```

If your database stored that exact hash,

the attacker instantly knew the password.

Salt makes those tables useless because every user's hash is different.

---

# Which Algorithm Should We Use?

Some common options:

| Algorithm | Status                              |
| --------- | ----------------------------------- |
| MD5       | Broken ❌                            |
| SHA1      | Broken ❌                            |
| SHA256    | Good for integrity, not passwords ❌ |
| bcrypt    | Good ✅                              |
| scrypt    | Good ✅                              |
| Argon2    | Excellent ✅                         |

---

# Why Argon2?

Argon2 won the **Password Hashing Competition (PHC)**.

It is designed to be:

* Slow to brute-force
* Memory-intensive
* Resistant to GPU attacks
* Recommended by security experts

For a new application, Argon2 is an excellent default choice.

---

# Installing the Library

We'll use **pwdlib**, which provides a modern interface and supports Argon2.

Install:

```bash
pip install pwdlib[argon2]
```

Update:

```bash
pip freeze > requirements.txt
```

---

# Implementing `security.py`

Remember we created:

```text
app/
└── core/
    └── security.py
```

Now we'll implement it.

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )
```

This file becomes the central place for password operations.

---

# Understanding Every Line

## Create the Password Hasher

```python
password_hash = PasswordHash.recommended()
```

This creates a hasher using current recommended settings (Argon2 at the time of writing).

---

## Hashing

```python
hash_password("MyPassword123")
```

Returns something like:

```text
$argon2id$v=19$m=65536,t=3,p=4$...
```

Notice:

Every call produces a different hash because a new random salt is generated each time.

---

# Verifying

Suppose the database stores:

```text
$argon2id$v=19...
```

User types:

```text
MyPassword123
```

We call:

```python
verify_password(
    "MyPassword123",
    stored_hash,
)
```

Returns:

```python
True
```

Wrong password:

```python
False
```

---

# Why Does Verification Work If Hashes Are Different Every Time?

This confuses many beginners.

Example:

First hash:

```text
Password123

↓

Hash A
```

Second hash:

```text
Password123

↓

Hash B
```

Different!

So how can verification work?

Because the stored hash contains:

* The salt
* The algorithm
* The parameters

During verification, the library extracts that information, hashes the entered password the same way, and compares the results.

You don't manage the salt manually.

---

# Registration Flow

```text
User Registers

↓

Enter Password

↓

hash_password()

↓

Store Hash

↓

Database
```

The plain password is discarded immediately.

---

# Login Flow

```text
User Logs In

↓

Enter Password

↓

verify_password()

↓

True / False

↓

Login or Reject
```

---

# Where Does This Fit?

Our authentication flow now looks like:

```text
Frontend

↓

POST /register

↓

Service

↓

hash_password()

↓

Repository

↓

Database
```

Login:

```text
Frontend

↓

POST /login

↓

Repository

↓

Get User

↓

verify_password()

↓

Success / Failure
```

---

# Common Beginner Mistakes

### ❌ Storing plain passwords

Never do this.

---

### ❌ Using SHA256 directly

SHA256 is fast.

Fast hashing is good for file integrity.

Fast hashing is bad for passwords because attackers can try billions of guesses quickly.

---

### ❌ Inventing your own hashing scheme

Never combine algorithms or create custom logic.

Use trusted libraries.

---

### ❌ Trying to decrypt passwords

You cannot decrypt a password hash.

Authentication relies on verification, not decryption.

---

# Project Structure

```text
app/
│
├── core/
│   ├── config.py
│   ├── security.py
│   └── logging.py
│
├── database/
├── models/
├── repositories/
├── services/
└── api/
```

`security.py` now contains all password-related functionality.

Later, we'll also place JWT helper functions in this file (or split them into a dedicated `jwt.py` module as the project grows).

---

# What You Learned Today

You now understand:

* Why passwords must never be stored in plain text
* Hashing vs encryption
* One-way functions
* Salting
* Rainbow table attacks
* Why Argon2 is recommended
* Password verification
* How to implement secure password hashing
* Where password security fits into your application's architecture

---

# Mini Challenge

Without looking back, answer these:

1. Why is storing plain text passwords dangerous?
2. What's the difference between hashing and encryption?
3. Why can't we decrypt a password hash?
4. What problem does salting solve?
5. Why do two users with the same password usually have different hashes?
6. Why is SHA256 not recommended for password storage?
7. What does `verify_password()` actually do?

If you can explain these concepts clearly, you've understood one of the most important security topics in backend development.

---

# Lesson 13 Preview — JWT Authentication

Now that passwords are secure, we'll build the rest of the authentication system.

You'll learn:

* What JWT (JSON Web Token) is
* Stateless authentication
* Access Tokens
* Refresh Tokens
* JWT structure (`Header.Payload.Signature`)
* Signing vs Encryption
* Token expiration
* Login and logout flow
* Protected routes
* Implementing authentication in FastAPI

By the end of Lesson 13, users will be able to register, log in, receive a JWT, and access protected endpoints in our AI Agent.
