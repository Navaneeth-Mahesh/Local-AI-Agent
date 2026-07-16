# Local AI Agent Platform

A production-grade Local AI Agent Platform that users can self-host on their own computers.

## Features

- JWT Authentication
- Refresh Tokens
- User Profiles
- User Settings
- AI Provider Configuration
- PostgreSQL
- SQLAlchemy 2.0
- FastAPI
- Docker Support
- Clean Architecture

## Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- JWT
- Pydantic

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI

## Folder Structure

```
backend/
frontend/
docs/
tests/
docker/
```

## Installation

```bash
git clone <repo>

cd backend

python -m venv .venv

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

## API Documentation

```
http://localhost:8000/docs
```

## License

MIT