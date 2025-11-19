FROM python:3.11-slim

# Evita buffering e força logs a aparecer no Render
ENV PYTHONUNBUFFERED=1

# Usa settings de produção
ENV DJANGO_SETTINGS_MODULE=plantao_pro.settings.prod

# Diretório principal
WORKDIR /app

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Coleta arquivos estáticos
RUN python manage.py collectstatic --noinput --settings=plantao_pro.settings.prod

# Comando de execução (o Render usa este CMD)
CMD ["gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]

