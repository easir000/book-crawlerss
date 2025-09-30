# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose API port
EXPOSE 8000

# Run API by default
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]