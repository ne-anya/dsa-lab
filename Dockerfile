FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirments.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirments.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app.py .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]