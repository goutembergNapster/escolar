#!/bin/bash
set -e

echo "=== APAGANDO QUALQUER STATICFILES ANTIGO (NUKE MODE) ==="
rm -rf /app/staticfiles
mkdir -p /app/staticfiles

echo "=== APAGANDO MANIFEST ANTIGO DO WHITENOISE (SE EXISTIR) ==="
find /app -name "staticfiles.json" -delete || true
find /tmp -name "staticfiles.json" -delete || true

echo "=== APAGANDO CACHE DO PYTHON/DJANGO ==="
find /app -name "__pycache__" -exec rm -rf {} +
find /app -name "*.pyc" -delete

echo "=== RODANDO MIGRATIONS ==="
python manage.py migrate --noinput --settings=plantao_pro.settings.prod

echo "=== RODANDO COLLECTSTATIC ==="
python manage.py collectstatic --clear --noinput --settings=plantao_pro.settings.prod

echo "=== INICIANDO SERVIDOR ==="
exec "$@"
