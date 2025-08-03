# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app source code
COPY . .

# Expose port Flask will run on
EXPOSE 8000

# Default command to run the Flask app
CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=8000"]
