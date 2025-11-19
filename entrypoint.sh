#!/bin/bash
set -e

echo "Rodando migrações..."
python manage.py migrate --noinput --settings=plantao_pro.settings.prod

echo "Coletando staticfiles..."
python manage.py collectstatic --noinput --settings=plantao_pro.settings.prod

echo "Iniciando servidor..."
exec "$@"