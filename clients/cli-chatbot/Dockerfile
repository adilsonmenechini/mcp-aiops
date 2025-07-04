FROM python:3.13-slim

# Evita perguntas interativas ao instalar pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza o apt e instala dependências para Node.js e Python
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    build-essential \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Instala Node.js LTS (com npm e npx incluídos)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY servers_config.json /app
COPY .env /app
COPY . /app