#!/bin/bash
set -e

echo "Rodando migrações..."
python manage.py migrate --noinput --settings=plantao_pro.settings.prod

echo "Limpando staticfiles antigo..."
rm -rf /app/staticfiles/*
rm -f /app/staticfiles/staticfiles.json

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=plantao_pro.settings.prod

echo "Criando superusuário padrão..."
python manage.py createinitialsuperuser --settings=plantao_pro.settings.prod

echo "Iniciando servidor..."
exec "$@"
