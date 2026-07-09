# AI Agent

> A production-grade, self-hosted AI Agent built with FastAPI, React, PostgreSQL, and Gemini.

Build your own intelligent AI assistant that runs entirely on your computer while giving you full control over your data, memory, tools, and permissions.

---

# Project Vision

The goal of this project is to build a production-grade AI Agent platform that anyone can self-host.

Each user can:

- Create an account
- Log in securely
- Connect their own Gemini API key
- Maintain private chat history
- Store long-term AI memory
- Index and search local files
- Configure personal settings
- Grant or deny permissions for sensitive actions
- Keep all data isolated from other users

Think of it as:

> **"An open-source Jarvis that anyone can run on their own computer."**

Unlike a simple chatbot, this project demonstrates real-world software engineering concepts including authentication, databases, AI integration, clean architecture, and frontend development.

---

# Project Goals

This project is designed to teach how modern AI applications are actually built.

Instead of hiding everything behind frameworks, we'll build the core systems ourselves and introduce libraries only when they solve real engineering problems.

By the end of the project, you'll understand every layer of the application—from the frontend to the AI engine.

---

# Tech Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- React Query
- React Router
- Framer Motion

---

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT Authentication

---

## AI

- Gemini API
- Google AI SDK

---

## Planned Integrations

### AI Providers

- Gemini
- Ollama *(Future)*
- OpenAI Compatible APIs *(Future)*

### Memory

- PostgreSQL
- pgvector
- ChromaDB *(Optional)*

### Search

- FAISS
- pgvector
- Sentence Transformers

### Background Jobs

- Redis
- Celery *(or Dramatiq)*

### File Monitoring

- Watchdog

---

# Core Features

## Authentication

- User Registration
- Login
- JWT Authentication
- Refresh Tokens
- Forgot Password *(Optional)*

---

## AI Chat

- Streaming Responses
- Markdown Support
- Code Highlighting
- Conversation History

---

## Memory System

- Short-Term Memory
- Long-Term Memory
- Semantic Search
- User Preferences

---

## Knowledge Base

Upload and chat with:

- PDF
- DOCX
- TXT
- Markdown

---

## Local File Search

Search indexed:

- Documents
- Source Code
- Notes

---

## Browser Tools

- Google Search
- Open Websites
- Summarize Web Pages

---

## System Tools

With user permission:

- Open Applications
- Create Folders
- Rename Files
- Delete Files
- Execute Terminal Commands

---

## Coding Assistant

- Explain Code
- Generate Code
- Review Projects
- Fix Bugs

---

## Voice

- Speech-to-Text
- Text-to-Speech

---

## Plugin System

Users can extend the AI Agent by creating custom tools.

---

## Settings

- Theme
- AI Provider
- API Keys
- Memory Configuration
- Permission Settings

---

# Permission System

Sensitive actions always require user approval.

Example:

```
AI wants to delete:

Downloads/test.txt
```

Available options:

- Allow Once
- Always Allow
- Deny

This prevents the AI from performing dangerous operations without explicit user consent.

---

# Project Structure

```text
AI-Agent/
│
├── frontend/
│
├── backend/
│
├── agent/
│   ├── brain/
│   ├── memory/
│   ├── tools/
│   ├── planner/
│   ├── permissions/
│   ├── prompts/
│   └── rag/
│
├── database/
│
├── docker/
│
├── docs/
│
├── tests/
│
└── README.md
```

---

# Development Roadmap

## Week 1

- Python Refresh
- FastAPI Fundamentals
- Project Setup
- Authentication
- Database Design

---

## Week 2

- Gemini Integration
- Chat Backend
- Streaming Responses
- Frontend Chat Interface

---

## Week 3

- Conversation History
- Memory System
- Embeddings
- Semantic Search

---

## Week 4

- Tool Calling
- Permission System
- Local File Access
- Browser Search
- Document Processing

---

## Week 5

- RAG
- Coding Assistant
- User Profiles
- Plugin Architecture
- Settings

---

## Week 6

- Voice Features
- Testing
- Docker
- Documentation
- Production Deployment

---

# What You'll Learn

## Python

- OOP
- Modules & Packages
- Async Programming
- Decorators
- Type Hints
- Context Managers

---

## Backend Development

- REST APIs
- Authentication
- Authorization
- Middleware
- Dependency Injection
- Validation

---

## AI Engineering

- Prompt Engineering
- Function Calling
- Tool Calling
- Context Windows
- Embeddings
- RAG
- Vector Search
- Agent Loops

---

## Databases

- SQL
- PostgreSQL
- SQLAlchemy ORM
- Relationships
- Transactions
- Alembic Migrations

---

## Software Architecture

- Clean Architecture
- Repository Pattern
- Service Layer
- SOLID Principles
- Dependency Injection

---

## DevOps

- Docker
- Environment Variables
- Logging
- Testing
- CI/CD
- Deployment

---

# What Makes This Project Different?

Instead of hardcoding tools into the AI Agent, we'll build a **Tool Registry**.

Each tool follows a common interface and registers itself with the agent.

For example:

- Browser Search
- File Search
- PDF Reader
- Terminal
- Calculator

Adding a new tool won't require changing the core AI engine.

This demonstrates extensibility, scalability, and clean software architecture.

---

# Development Philosophy

This is **not** an AI demo.

It is a production-style software engineering project.

Throughout the project we'll focus on:

- Clean, modular code
- Small and meaningful Git commits
- Proper documentation
- Scalable architecture
- Automated testing
- Understanding every concept before using libraries

---

# Getting Started

## Clone the Repository

```bash
git clone <repository-url>

cd AI-Agent
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Project Status

🚧 Currently under active development.

Features are being built incrementally while maintaining production-quality architecture and documentation.

---

# License

This project is licensed under the MIT License.