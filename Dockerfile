FROM python:3.13-slim

# Install pip build dependencies
RUN apt-get update && apt-get install -y build-essential

# Set work directory
WORKDIR /app

# Copy pyproject.toml and lockfile (generated via uv or poetry locally)
COPY pyproject.toml .
COPY uv.lock ./

# Install pip backend (e.g., pip can now understand pyproject.toml via `pip install .`)
RUN pip install --upgrade pip setuptools wheel
RUN pip install .

# Copy source
COPY . .
