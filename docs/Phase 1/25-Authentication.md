# Authentication

Authentication is the process of verifying **who a user is** before allowing them to access the application.

Think of authentication as showing your ID card before entering a secure building.

Without authentication, the server has no way of knowing who is making a request.

Our AI Agent will use **JWT (JSON Web Token)** based authentication, which is the most common authentication method for modern web applications.

---

# Why Do We Need Authentication?

Imagine our AI Agent without authentication.

Anyone could:

- View another user's chat history
- Access personal memories
- Use someone else's Gemini API key
- Modify settings
- Delete conversations

Authentication prevents unauthorized users from accessing protected resources.

Every user gets their own private account and data.

---

# Authentication Flow

When a user logs in, the process looks like this:

```text
User

↓

Enter Email & Password

↓

Backend verifies credentials

↓

JWT Access Token generated

↓

Frontend stores token

↓

Frontend sends token with every request

↓

Backend verifies token

↓

Access granted
```

Once the user is authenticated, they don't need to enter their password for every request.

Instead, they use the JWT token.

---

# JWT Authentication

JWT stands for **JSON Web Token**.

It is a compact, secure token that proves a user's identity after they log in.

Instead of sending a username and password with every request, the frontend sends the JWT token.

Example:

```text
Login

↓

Access Token Generated

↓

Token sent to Frontend

↓

Frontend stores token

↓

Future requests include the token
```

JWT authentication is:

- Stateless
- Fast
- Secure
- Widely used in REST APIs

---

# What Does a JWT Look Like?

A JWT is simply a long encoded string.

Example:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Although it looks random, it actually contains three parts.

```text
Header

.

Payload

.

Signature
```

---

## Header

The header describes how the token was created.

Example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

It specifies:

- Token type
- Signing algorithm

---

## Payload

The payload contains user-related information called **claims**.

Example:

```json
{
    "sub": "1"
}
```

Here:

- `sub` means **Subject**
- It usually stores the user's unique ID.

Later, we'll also include information like expiration time.

---

## Signature

The signature is created using a secret key stored on the server.

Its purpose is to ensure the token hasn't been modified.

If someone changes even one character in the token, the signature becomes invalid and the backend rejects the request.

---

# Access Token

An Access Token is the token used to access protected resources.

Example:

```text
User logs in

↓

Backend generates Access Token

↓

Frontend stores it

↓

Sent with every request
```

The access token is usually short-lived.

Example:

```
15 minutes

30 minutes

1 hour
```

Short expiration times reduce security risks if the token is stolen.

---

# Refresh Token

A Refresh Token is used to generate a new Access Token without asking the user to log in again.

Instead of forcing users to enter their password every few minutes, the backend issues a Refresh Token during login.

Flow:

```text
Login

↓

Access Token

+

Refresh Token

↓

Access Token expires

↓

Frontend sends Refresh Token

↓

Backend verifies it

↓

New Access Token issued
```

Refresh tokens usually live much longer than access tokens.

For example:

- 7 days
- 30 days
- 90 days

In our project, refresh tokens will also be stored in the database so they can be revoked if needed.

---

# Access Token vs Refresh Token

| Feature | Access Token | Refresh Token |
|----------|--------------|---------------|
| Purpose | Access protected APIs | Generate a new access token |
| Lifetime | Short | Long |
| Sent with every request | Yes | No |
| Stored in database | Usually No | Yes (in our project) |
| Used after login | Yes | Only when access token expires |

---

# Authorization Header

Once the user logs in, every protected request must include the Access Token.

The token is sent inside the HTTP Authorization header.

Example:

```http
GET /users/me

Authorization: Bearer eyJhbGc...
```

The backend reads this header, verifies the token, and identifies the user.

---

# What Does "Bearer" Mean?

You'll often see:

```http
Authorization: Bearer <token>
```

The word **Bearer** simply tells the server:

> "The client is presenting this token as proof of authentication."

The format is always:

```text
Authorization: Bearer <access_token>
```

Without the `Bearer` prefix, the backend won't recognize the token correctly.

---

# Protected Endpoints

Not every API requires authentication.

Some endpoints are public.

Example:

```text
POST /auth/register

POST /auth/login
```

Anyone can access these because users need them before logging in.

Other endpoints contain private user data.

These are called **Protected Endpoints**.

Only authenticated users can access them.

Examples:

```text
GET /users/me

GET /settings

POST /ai-provider
```

If the request does not contain a valid JWT, the backend returns:

```http
401 Unauthorized
```

---

# Example Request

### Login

```http
POST /auth/login
```

Response:

```json
{
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

---

### Access Protected Endpoint

```http
GET /users/me
Authorization: Bearer eyJhbGc...
```

If the token is valid:

```json
{
    "id": 1,
    "username": "Navaneeth",
    "email": "nav@gmail.com"
}
```

If the token is invalid or expired:

```http
401 Unauthorized
```

---

# Complete Authentication Flow

```text
User

↓

Login

↓

Backend verifies email & password

↓

Generate Access Token

↓

Generate Refresh Token

↓

Return tokens

↓

Frontend stores tokens

↓

User requests protected endpoint

↓

Authorization: Bearer <Access Token>

↓

Backend verifies JWT

↓

Access granted

↓

If Access Token expires

↓

Frontend sends Refresh Token

↓

Backend verifies Refresh Token

↓

New Access Token generated

↓

User continues without logging in again
```

---

# Why Are We Using JWT?

JWT authentication is widely used because it offers several advantages:

- Stateless authentication (the server doesn't need to store user sessions)
- Fast token verification
- Easy integration with frontend applications
- Secure when implemented correctly
- Works well with REST APIs and mobile applications
- Scales efficiently for large applications

---

# Key Takeaways

After this lesson, you should understand:

- What authentication is and why it's important
- How JWT authentication works
- The difference between Access Tokens and Refresh Tokens
- The purpose of the Authorization header
- Why the `Bearer` prefix is required
- What protected endpoints are
- How the complete login and authentication flow works in a production application