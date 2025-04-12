# Build stage using uv
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set working directory
WORKDIR /build

# Copy the project configuration files
COPY pyproject.toml uv.lock ./

# Copy application code
COPY shelly-to-postgres/ ./shelly-to-postgres/

# Install dependencies with uv, frozen to ensure reproducibility
RUN uv sync --frozen --no-editable

# Final stage
FROM python:3.13-alpine

# Create non-root user with UID 1000
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy Python virtual environment from builder stage (contains all dependencies)
COPY --from=builder --chown=appuser:appgroup /build/.venv /app/.venv

# Copy application code from builder stage
COPY --from=builder --chown=appuser:appgroup /build/shelly-to-postgres /app

# Switch to non-root user
USER 1000

# Add virtual environment bin directory to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["python", "main.py"]
