# Use official Python image with tag matching project's minimum requirement
FROM python:3.13-slim

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

# Copy only dependency files first for layer caching
COPY pyproject.toml README.md /app/

# Install pip-tools for PEP 517 builds if needed, then install dependencies
RUN pip install --no-cache-dir pip wheel
RUN pip install --no-cache-dir "fast-alpr[onnx]>=0.3.0" "fastapi[standard]"

# Copy app source
COPY . /app

# Expose port used by Uvicorn (80 for convenience)
EXPOSE 80

# Run with Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
