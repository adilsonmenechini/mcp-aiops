FROM python:3.12-slim-bullseye

WORKDIR /app
COPY requirements.txt .
COPY . .

RUN pip install --no-cache-dir -r requirements.txt