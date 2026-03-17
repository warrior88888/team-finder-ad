# Use a Python image with uv pre-installed
FROM astral/uv:python3.13-bookworm-slim

# Install gosu for privilege dropping at runtime
RUN apt-get update && apt-get install -y --no-install-recommends gosu \
    && rm -rf /var/lib/apt/lists/*

# Setup a non-root user
RUN groupadd --system --gid 999 django \
 && useradd --system --gid 999 --uid 999 --create-home django

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Copy entrypoint and create required directories
# entrypoint runs as root to fix volume permissions at runtime, then drops to django via gosu
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && mkdir -p /app/collected_static /app/media /var/log/django

# Run entrypoint as root (it will drop to django internally via gosu)
ENTRYPOINT ["entrypoint.sh"]

# Run Django App using Gunicorn (launched via gosu inside entrypoint)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "team_finder.wsgi", "--workers", "3"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD gosu django python manage.py health_check health_check || exit 1