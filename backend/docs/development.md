# Development

Run Server

uvicorn app.main:app --reload

Create Migration

alembic revision --autogenerate -m "message"

Apply Migration

alembic upgrade head

Run Tests

pytest