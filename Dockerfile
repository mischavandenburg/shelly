# Build stage
FROM python:3.13-alpine AS builder

# Set working directory
WORKDIR /build

# Copy requirements file
COPY requirements.txt .

# Install dependencies to a specific directory
RUN pip install --no-cache-dir --target=/build/packages -r requirements.txt

# Copy application code
COPY shelly-to-postgres/ ./app/

# Final stage
FROM python:3.13-alpine

# Create non-root user with UID 1000
RUN addgroup -g 1000 -S appgroup && \
    adduser -u 1000 -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /build/packages /app/packages

# Copy application code from builder stage
COPY --from=builder /build/app /app

# Set ownership for app directory
RUN chown -R appuser:appgroup /app

# Set Python path to include packages directory
ENV PYTHONPATH=/app/packages

# Switch to non-root user
USER 1000

# Run the application
CMD ["python", "main.py"]
