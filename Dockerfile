FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências necessárias para psycopg2, Pillow e outros
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# NÃO roda collectstatic no build (somente no runtime)
# Render roda isso automaticamente se você usar entrypoint.

# Entrypoint separado para fazer:
# - migrações
# - collectstatic
# - rodar gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]
