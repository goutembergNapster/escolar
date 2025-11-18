# ---- Base ----
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# instalar dependências do sistema se precisar (psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# instalar dependências pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copiar o projeto
COPY . .

# coletar static em build
RUN python manage.py collectstatic --noinput

# expor porta
EXPOSE 8000

# rodar gunicorn
CMD ["gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]


