FROM python:3.9-slim

# Install system dependencies
# curl is needed for the download script
# libmagic1 and poppler-utils are needed for the python dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libmagic1 \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project configuration
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project

# Copy the scripts
COPY extract_pdf_text.py download.sh ./

# Make sure the download script is executable
RUN chmod +x download.sh

# Set the entrypoint
ENTRYPOINT ["./download.sh"]
