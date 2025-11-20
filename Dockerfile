# Imagem base
FROM python:3.11-slim

# Diretório da aplicação
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt-get clean

# Copia requirements antes (cache melhor)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Coletar arquivos estáticos ANTES do entrypoint
RUN python manage.py collectstatic --noinput

# Copia entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Porta da aplicação
EXPOSE 8000

# Comando padrão
CMD ["/entrypoint.sh", "gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]
