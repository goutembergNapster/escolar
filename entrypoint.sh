#!/bin/bash

echo "Rodando migrações..."
python manage.py migrate --noinput --settings=plantao_pro.settings.prod

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=plantao_pro.settings.prod

echo "Iniciando servidor..."
exec "$@"
