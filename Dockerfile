# Use official Python image with tag matching project's minimum requirement
FROM python:3.13-slim

# Install uv specifically
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set a working directory
WORKDIR /app

# Install system dependencies useful for image decoding and OpenCV (if used)
# Keep layers small and clean
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        ffmpeg \
        libgl1 \
    && rm -rf /var/lib/apt/lists/*
    
# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies without copying the whole project yet
# --frozen ensures we use the exact lockfile versions
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Place the uv-created virtualenv on the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 80

# Run with Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
