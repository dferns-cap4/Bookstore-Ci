#!/bin/bash
set -e

# Wait for the database to be ready
until pg_isready -h db -p 5432 -U fastapi_user; do
  echo "Waiting for the database to be ready..."
  sleep 2
done

# Initialize the database schema
echo "Initializing database schema..."
python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"

# Run tests
echo "Running tests..."
pytest tests/
