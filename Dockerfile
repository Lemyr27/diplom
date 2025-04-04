FROM python:3.11-slim-bookworm AS builder

ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev --no-interaction --no-ansi


FROM python:3.11-slim-bookworm

COPY --from=builder app/ app/

WORKDIR /app

COPY app/ app/

CMD ["/app/.venv/bin/uvicorn", "app.entrypoints.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
