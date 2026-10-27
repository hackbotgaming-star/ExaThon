FROM python:3.12-slim

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    pandas \
    numpy \
    scipy \
    scikit-learn \
    duckdb \
    pyexasol \
    python-pptx \
    reportlab \
    python-multipart \
    pytest

# Copy application code
COPY . .

# Generate sample datasets if not present
RUN python data/generation/generate_retail_data.py

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
