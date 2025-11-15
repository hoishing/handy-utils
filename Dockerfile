FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files
COPY uv.lock pyproject.toml $HOME/app

# Install Python dependencies with uv
RUN uv sync --frozen || uv sync

# Copy application code
COPY . .

# Expose port
EXPOSE 8211

# Run the application
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8211", "--server.address=0.0.0.0"]
