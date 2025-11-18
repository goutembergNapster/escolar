FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=plantao_pro.settings.prod

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# coletar estáticos no momento do build
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "plantao_pro.wsgi:application", "--bind", "0.0.0.0:8000"]
