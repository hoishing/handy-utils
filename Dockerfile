FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency files
COPY --chown=user uv.lock pyproject.toml $HOME/app

# Install Python dependencies with uv
RUN uv sync --frozen || uv sync

# Copy application code
COPY --chown=user . $HOME/app
# Expose port
EXPOSE 8211

# Run the application
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8211", "--server.address=0.0.0.0"]
