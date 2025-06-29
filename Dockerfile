FROM deps:latest

WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock README.md ./
# Copy application code (early)
COPY src/ ./src/

# Install dependencies (packages already exist)
RUN poetry install

# Set default command
CMD ["uvicorn", "demo_ai.main:app", "--host", "0.0.0.0", "--port", "8000"]
