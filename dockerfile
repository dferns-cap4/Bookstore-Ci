FROM python:3.10-slim

# Set a directory for the app
WORKDIR /usr/src/app

# Install system dependencies (including postgresql-client)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application's port
EXPOSE 8000

# Default command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
