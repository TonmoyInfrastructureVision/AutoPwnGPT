# AutoPwnGPT Dockerfile

Author: Eshan Roy
Email: m.eshanized@gmail.com
GitHub: https://github.com/TonmoyInfrastructureVision
Date: 2025-04-22

FROM python:3.10-slim

LABEL maintainer="Eshan Roy <m.eshanized@gmail.com>"
LABEL description="AutoPwnGPT - AI-powered penetration testing framework"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p data/logs data/reports data/sessions data/payloads

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AUTOPWNGPT_ENV=production

# Expose port for web interface
EXPOSE 8080

# Run the application
ENTRYPOINT ["python", "src/main.py"]

# Default command (can be overridden)
CMD ["--help"]
