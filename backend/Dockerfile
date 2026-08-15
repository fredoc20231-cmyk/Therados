FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

COPY therados /app/therados
COPY alembic.ini /app/
COPY alembic /app/alembic

EXPOSE 8000

CMD ["uvicorn", "therados.main:app", "--host", "0.0.0.0", "--port", "8000"]
