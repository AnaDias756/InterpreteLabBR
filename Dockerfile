FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements-backend.txt .
RUN pip install --no-cache-dir -r requirements-backend.txt

# Copiar código da aplicação
COPY backend/ ./backend/
COPY data/ ./data/
COPY .env* ./ || true

# Expor porta (Render define automaticamente)
EXPOSE 10000

# Comando para iniciar a aplicação
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}