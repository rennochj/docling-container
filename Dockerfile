# Multi-stage Dockerfile for docling-forge
# Stage 1: Build and install dependencies using uv
FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files (including lock file for reproducible builds)
COPY pyproject.toml uv.lock ./

# Copy application code (needed for package installation)
COPY docling_forge/ ./docling_forge/

# Install dependencies using uv sync
# This creates a .venv directory and uses the lock file for exact dependency versions
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync --frozen --no-dev


# Stage 2: Runtime image
FROM python:3.13-slim

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/docling_forge /app/docling_forge

# Set environment variables
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create directories for input and output
RUN mkdir -p /input /output

# Set working directory
WORKDIR /app

# Copy model prefetch script
COPY scripts/prefetch-models.py /tmp/prefetch-models.py

# Pre-download RapidOCR models to avoid runtime downloads
# This improves first-run performance and ensures models are available offline
RUN /app/.venv/bin/python /tmp/prefetch-models.py && rm /tmp/prefetch-models.py

# Default volumes
VOLUME ["/input", "/output"]

# Set the entrypoint to the CLI
ENTRYPOINT ["python", "-m", "docling_forge.main"]

# Default command shows help
CMD ["--help"]
