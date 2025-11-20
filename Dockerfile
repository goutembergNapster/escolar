# Usando Python slim
FROM python:3.11-slim

# Diretório da aplicação
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Copia requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia projeto
COPY . .

# Copia entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expondo a porta
EXPOSE 8000

CMD ["/entrypoint.sh", "gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]
