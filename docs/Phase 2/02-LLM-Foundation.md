# Phase 2 — Lesson 2 (Part A)

# Building the LLM Foundation

> **Objective:** Build the core foundation of our AI engine by creating provider-independent models, interfaces, enums, and exceptions. At the end of this lesson, our application will know **how to communicate with any LLM**, without depending on Gemini, OpenAI, or Ollama.

---

# Why Are We Doing This?

A common beginner approach is to directly use an AI provider throughout the project.

Example:

```python
from google import genai

client = genai.Client()
response = client.models.generate_content(...)
```

This works for small projects.

However, imagine six months later:

- You want to switch from Gemini to OpenAI.
- A company wants to use Ollama locally.
- Another customer prefers Claude.

If Gemini-specific code exists throughout the project, changing providers becomes difficult.

Instead, we will build our own AI layer.

The rest of our application will never know which AI provider is being used.

---

# Our Architecture

```
Chat Service
      │
      ▼
LLM Service
      │
      ▼
Base LLM Provider
      │
      ▼
Gemini Provider
```

Later, we can simply replace Gemini.

```
Chat Service
      │
      ▼
LLM Service
      │
      ▼
Base LLM Provider
      │
      ▼
OpenAI Provider
```

Notice something important:

Only the provider changes.

Everything above it remains exactly the same.

---

# Why Keep AI in a Separate `agent/` Module?

Instead of placing AI inside `app/`, we'll create a dedicated module.

```
backend/

├── app/
│
└── agent/
```

## app/

Contains backend logic:

- Authentication
- APIs
- Database
- Business logic
- Services

Think of it as:

> "How users interact with the application."

---

## agent/

Contains everything related to AI.

Examples:

- LLMs
- Memory
- Planning
- Tools
- RAG
- Embeddings
- Context Management

Think of it as:

> "How the AI thinks and performs tasks."

Keeping these separate makes the project easier to understand, maintain, and extend.

---

# Folder Structure

After this lesson, our project will contain:

```text
backend/
└── agent/
    └── llm/
        ├── __init__.py
        ├── enums.py
        ├── exceptions.py
        ├── interfaces.py
        └── models.py
```

Each file has one clear responsibility.

---

# File Overview

| File | Responsibility |
|------|----------------|
| `__init__.py` | Exposes public classes for easier imports |
| `enums.py` | Stores shared enums like roles and provider types |
| `models.py` | Defines our own request and response models |
| `interfaces.py` | Defines the contract every provider must implement |
| `exceptions.py` | Stores common LLM-related exceptions |

This follows the **Single Responsibility Principle**.

---

# 1. `__init__.py`

**File Path**

```text
backend/agent/llm/__init__.py
```

## Purpose

This file acts as the public entry point for the `llm` package.

Instead of writing:

```python
from agent.llm.interfaces import BaseLLMProvider
from agent.llm.models import LLMRequest
```

we can simply write:

```python
from agent.llm import BaseLLMProvider, LLMRequest
```

This keeps imports cleaner and hides the internal folder structure.

---

# 2. `enums.py`

**File Path**

```text
backend/agent/llm/enums.py
```

## What is an Enum?

An **Enum (Enumeration)** is a fixed collection of predefined values.

Instead of using random strings:

```python
"user"

"assistant"

"system"
```

we define them once.

```python
class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
```

Now, throughout the project, we use:

```python
MessageRole.USER
```

instead of:

```python
"user"
```

---

## Why Use Enums?

Without enums:

```python
"Assistant"

"assistant"

"ASSISTANT"

"assisstant"
```

Even one typo can cause bugs.

Enums provide:

- Type safety
- Auto-completion
- Consistency
- Fewer bugs

---

## ProviderType

Another enum stores supported providers.

```python
ProviderType

↓

Gemini

OpenAI

Ollama
```

Later, when we add new providers, we simply extend this enum.

---

# 3. `models.py`

**File Path**

```text
backend/agent/llm/models.py
```

## Why Create Our Own Models?

Every AI provider has different request and response formats.

Gemini:

```
contents
parts
candidate
```

OpenAI:

```
messages
choices
content
```

Claude:

```
content
text
```

If we use those models directly, our application becomes tied to one provider.

Instead, we create our own common models.

```
LLMRequest

↓

Provider

↓

LLMResponse
```

Every provider converts its own format into these models.

This is called a **Canonical Domain Model**.

---

## LLMMessage

Represents one message in a conversation.

Example:

```
User:
Hello

Assistant:
Hi!

User:
Teach me Python
```

Each message contains:

- Role
- Content

---

## LLMRequest

Represents everything needed to send a request to an AI model.

Contains:

- Messages
- Temperature
- Max Tokens
- Stream

---

### Temperature

Controls randomness.

```
0.0

↓

More predictable

↓

More factual
```

```
2.0

↓

More creative

↓

Less predictable
```

Common values:

```
0.2 → Coding

0.5 → General Chat

0.7 → Balanced

1.0 → Creative Writing
```

---

### Max Tokens

Limits the length of the response.

Example:

```
Max Tokens = 100

↓

The model cannot generate more than approximately 100 tokens.
```

This helps control:

- Cost
- Response length

---

### Stream

Determines how responses are returned.

False:

```
Wait...

↓

Entire response appears at once.
```

True:

```
Hello

↓

How

↓

are

↓

you?
```

Streaming provides a much better user experience.

---

## LLMResponse

Represents a provider-independent response.

Contains:

- Generated content
- Model name
- Usage information

Every provider converts its response into this format.

---

## LLMUsage

Stores token usage.

Example:

```
Prompt Tokens

Completion Tokens

Total Tokens
```

Useful for:

- Monitoring costs
- Analytics
- Usage limits

---

# 4. `interfaces.py`

**File Path**

```text
backend/agent/llm/interfaces.py
```

## What is an Interface?

An interface defines a contract.

It says:

> "Every LLM provider must implement these methods."

For now, our interface contains only one method.

```
generate()
```

Every provider must implement it.

```
GeminiProvider

↓

generate()
```

```
OpenAIProvider

↓

generate()
```

```
OllamaProvider

↓

generate()
```

Because they all follow the same contract, the rest of the application can use any provider without knowing which one it is.

---

## Why Only One Method?

Beginners often create large interfaces immediately.

Example:

```
generate()

stream()

vision()

embedding()

audio()

tools()

speech()

...
```

Professional systems don't.

They begin with the smallest stable contract and expand only when needed.

This follows the **Interface Segregation Principle (SOLID)**.

---

# 5. `exceptions.py`

**File Path**

```text
backend/agent/llm/exceptions.py
```

## Why Create Our Own Exceptions?

Every SDK throws different errors.

Gemini:

```
GoogleAuthError
```

OpenAI:

```
OpenAIAuthenticationError
```

Instead of exposing provider-specific errors to the application, we define our own.

```
AuthenticationError
```

Now every provider converts its own errors into common exceptions.

```
Google Error

↓

AuthenticationError
```

```
OpenAI Error

↓

AuthenticationError
```

This keeps the rest of the application provider-independent.

---

# What We Built

After this lesson, we have built the foundation of our LLM layer.

```
Chat Service

↓

LLM Service

↓

BaseLLMProvider

↓

Gemini Provider (Later)
```

At this stage:

- No Gemini SDK
- No API calls
- No business logic

Only the common foundation that every provider will follow.

---

# Project Structure

```text
backend/
└── agent/
    └── llm/
        ├── __init__.py
        ├── enums.py
        ├── exceptions.py
        ├── interfaces.py
        └── models.py
```

---

# Key Concepts Learned

- Why AI code should be separated from backend logic.
- Why provider-specific code should never leak into the application.
- What a Canonical Domain Model is.
- Why Enums improve consistency and type safety.
- Why Interfaces enable provider independence.
- Why custom Exceptions create a clean abstraction layer.
- How this architecture follows Clean Architecture and SOLID principles.

---

# What's Next?

In **Lesson 2 – Part B**, we'll build our first real provider.

We'll implement:

- Gemini Client
- Gemini Provider
- Request Mapper
- Response Mapper
- Error Handling

This will be the only place in the project that imports:

```python
from google import genai
```

Every other part of the application will continue using only our own abstraction layer.

---
