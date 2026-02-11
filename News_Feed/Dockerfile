# Stage 1: Builder stage
FROM python:3.11-slim-bullseye AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies required for psycopg2, numpy, matplotlib
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (leverages Docker cache)
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Stage 2: Final stage
FROM python:3.11-slim-bullseye

# Create non-root user
RUN addgroup --system --gid 1000 django && \
    adduser --system --uid 1000 --gid 1000 django

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/django/.local/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache /wheels/*

# Create and set work directory
WORKDIR /app

# Copy project files
COPY --chown=django:django . .

# Create staticfiles directory with proper permissions
RUN mkdir -p /app/staticfiles && chown -R django:django /app/staticfiles

# Switch to non-root user
USER django

# Run gunicorn
CMD gunicorn --bind 0.0.0.0:8000 News_Feed.wsgi:application