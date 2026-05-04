FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Verify gunicorn installed
RUN gunicorn --version

COPY . .

RUN mkdir -p data

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV PORT=8080

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 300 wsgi:application