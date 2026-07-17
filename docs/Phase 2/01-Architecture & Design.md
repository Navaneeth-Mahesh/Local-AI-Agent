# Building the LLM Abstraction Layer (Part 1: Architecture & Design)

> **Objective:** Build a provider-independent AI layer so the rest of the application never depends directly on Gemini, OpenAI, Claude, Ollama, or any vendor SDK.

---

# Why This Lesson Matters

When beginners build AI applications, they usually write code like this:

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(...)
```

This works for a demo.

But imagine your application grows to **100+ files**.

Now Gemini is imported everywhere.

```
chat.py

conversation.py

memory.py

planner.py

rag.py

tools.py

agents.py
```

Every module talks directly to Gemini.

Now your customer says:

> "We want OpenAI instead."

You now have to search your entire project and replace Google-specific code.

Professional software avoids this problem by introducing an **abstraction layer**.

---

# What is an Abstraction Layer?

An abstraction layer is a middle layer that hides implementation details.

Instead of every part of the application talking directly to Gemini, everything talks to a common interface.

Think of it like a universal remote.

```
TV Remote

↓

Universal Commands

↓

Samsung TV

or

Sony TV

or

LG TV
```

The buttons on the remote never change.

Only the internal implementation changes.

The same idea applies to AI providers.

---

# Without an Abstraction Layer

```
Chat Service
      │
      ▼
 Gemini SDK
```

Looks simple.

But soon:

```
Chat

↓

Gemini

Conversation

↓

Gemini

Memory

↓

Gemini

Planner

↓

Gemini

Tool Executor

↓

Gemini
```

Now your application is tightly coupled.

Problems appear everywhere.

---

# With an Abstraction Layer

```
Chat

↓

LLM Service

↓

Provider Interface

↓

Gemini Provider
```

Later:

```
Chat

↓

LLM Service

↓

Provider Interface

↓

OpenAI Provider
```

Notice something important.

The Chat Service never changed.

Only the provider changed.

---

# Real-Life Analogy

Imagine a restaurant.

Customers don't go into the kitchen.

They talk to the waiter.

```
Customer

↓

Waiter

↓

Kitchen
```

If the chef changes...

The customer doesn't care.

If the menu changes...

The customer still talks to the waiter.

In our application:

```
Customer

=

Chat Service

Waiter

=

LLM Service

Kitchen

=

Gemini/OpenAI/Ollama
```

The waiter hides all kitchen details.

---

# Why Not Import Gemini Everywhere?

Because vendor SDKs are implementation details.

The application should only know business concepts.

Bad:

```python
response.candidates[0].content.parts[0].text
```

Good:

```python
response.text
```

The application shouldn't care how Gemini structures responses.

That's the provider's responsibility.

---

# Dependency Inversion Principle (SOLID)

One of the five SOLID principles is:

> High-level modules should not depend on low-level modules.

Instead:

Both depend on abstractions.

Bad:

```
Conversation Service

↓

Gemini SDK
```

Good:

```
Conversation Service

↓

LLM Interface

↓

Gemini Provider
```

Conversation Service knows nothing about Google.

---

# Open/Closed Principle

Professional software should be:

Open for extension.

Closed for modification.

Meaning:

You should be able to add:

```
Claude

OpenAI

Ollama

Azure OpenAI
```

without editing:

```
Conversation Service

Chat Service

Memory

Planner
```

You only add another provider.

---

# High-Level Architecture

```
Frontend

↓

Chat API

↓

Chat Service

↓

Conversation Service

↓

LLM Service

↓

LLM Factory

↓

Provider Interface

↓

Gemini Provider

↓

Google SDK

↓

Gemini API
```

Each layer has only one responsibility.

---

# Responsibility of Every Layer

## Frontend

Responsible for:

* Sending messages
* Showing streamed responses
* Displaying conversation history

Never calls Gemini directly.

---

## Chat API

Responsible for:

* Authentication
* Receiving requests
* Returning responses

No AI logic.

---

## Chat Service

Responsible for:

* Chat workflow
* Validating conversation
* Saving messages
* Calling LLM Service

No provider-specific code.

---

## LLM Service

Responsible for:

* Public AI interface
* Error handling
* Logging
* Retry logic
* Calling the correct provider

This becomes the gateway to all AI operations.

---

## Factory

Responsible for selecting the correct provider.

Example:

```
User Settings

↓

Provider = Gemini

↓

GeminiProvider
```

Tomorrow:

```
Provider = Ollama

↓

OllamaProvider
```

Nothing else changes.

---

## Provider

Responsible for:

* SDK initialization
* API requests
* API response conversion
* Streaming
* Embeddings
* Model listing

Everything vendor-specific stays here.

---

# Canonical Domain Model

Every provider returns different response formats.

Gemini:

```
candidate

parts

text
```

OpenAI:

```
choices

message

content
```

Claude:

```
content

text
```

Instead of exposing those differences to the application, we define our own common models.

```
LLMRequest

↓

Provider

↓

Gemini/OpenAI Response

↓

LLMResponse
```

Every provider converts its own response into the same format.

This is called a **Canonical Domain Model**.

---

# Folder Structure Explained

```
app/

└── llm/

    interfaces.py
```

Defines what every provider **must** implement.

Think of it as a contract.

---

```
models.py
```

Defines shared request and response models.

No Google imports.

No OpenAI imports.

---

```
exceptions.py
```

Contains common exceptions used across the application.

Instead of catching:

```
GoogleAuthenticationError
```

we catch:

```
AuthenticationError
```

Much cleaner.

---

```
enums.py
```

Stores shared enums like:

```
ProviderType

Role

FinishReason
```

---

```
providers/
```

Contains provider implementations.

Each provider knows only its own SDK.

---

```
factory.py
```

Creates the correct provider based on configuration.

---

```
service.py
```

Public interface used by the application.

Every module uses:

```
LLMService
```

Never:

```
GeminiProvider
```

---

```
dependencies.py
```

FastAPI Dependency Injection.

Instead of manually creating services:

```python
service = LLMService(...)
```

FastAPI automatically injects it.

---

# Benefits of This Architecture

✔ Easy to switch AI providers

✔ Better testing

✔ Centralized configuration

✔ Cleaner codebase

✔ Follows SOLID principles

✔ Easier maintenance

✔ Easier debugging

✔ Supports enterprise deployments

✔ Prevents vendor lock-in

✔ Scales as the project grows

---

# Future Expansion

Because we designed the architecture correctly, adding a new provider later is simple.

```
providers/

    gemini.py

    openai.py

    claude.py

    ollama.py

    azure.py
```

The rest of the application remains unchanged.

---

# Summary

By the end of this lesson, you understand:

* Why abstraction layers are essential in production software.
* How dependency inversion reduces coupling.
* Why applications should depend on interfaces instead of SDKs.
* How a canonical domain model provides a consistent API across different LLM providers.
* The responsibility of every layer in the AI architecture.
* Why `LLMService` becomes the single entry point for all AI operations.
* How this design makes the project scalable, testable, and easy to maintain.

---

# Key Takeaways

* **Never import a vendor SDK outside its provider implementation.**
* **The rest of the application should only communicate with `LLMService`.**
* **All providers must implement the same interface.**
* **The application owns the domain models (`LLMRequest`, `LLMResponse`, etc.), not the AI vendor.**
* **Adding a new provider should require creating a new provider class, not modifying existing business logic.**
* **This architecture follows Clean Architecture and all five SOLID principles, making it suitable for real-world production systems.**

This expanded version is much closer to professional engineering documentation. It explains not only the architecture, but also the reasoning behind each design decision, making it a valuable reference when you revisit the project months later.
