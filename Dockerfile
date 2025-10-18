# Multi-stage Dockerfile for docling-container
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

# Copy dependency files
COPY pyproject.toml ./

# Create virtual environment and install dependencies
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache -r pyproject.toml

# Copy application code
COPY docling_container/ ./docling_container/

# Install the package
RUN uv pip install --no-cache -e .


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
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --from=builder /app/docling_container /app/docling_container

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Create directories for input and output
RUN mkdir -p /input /output

# Set working directory
WORKDIR /app

# Default volumes
VOLUME ["/input", "/output"]

# Set the entrypoint to the CLI
ENTRYPOINT ["python", "-m", "docling_container.main"]

# Default command shows help
CMD ["--help"]
