#!/bin/sh
set -e

echo ""
echo "==============================="
echo "🚀 ENTRYPOINT — Iniciando"
echo "==============================="
echo ""

# ------------------------------------------------------------
# 0) Esperar Postgres usando a DATABASE_URL do .env
# ------------------------------------------------------------
if [ -n "$DATABASE_URL" ]; then
    echo "⏳ Aguardando Postgres em: $DATABASE_URL"
    /scripts/wait_psql.sh "$DATABASE_URL"
else
    echo "⚠️  DATABASE_URL não definido. Continuando sem esperar Postgres..."
fi

echo ""
echo "==============================="
echo "🔧 Ambiente"
echo "==============================="
echo "DJANGO_ENV        = ${DJANGO_ENV:-dev}"
echo "DJANGO_SETTINGS   = plantao_pro.settings.dev"
echo "Python version    = $(python -V 2>&1)"
echo "Pip version       = $(pip -V 2>&1)"
echo ""

# ------------------------------------------------------------
# 1) Rodar migrations
# ------------------------------------------------------------
echo "📦 Rodando migrations..."
python manage.py migrate --noinput --settings=plantao_pro.settings.dev
echo "✔️ Migrations aplicadas!"
echo ""

# ------------------------------------------------------------
# 2) Criar superuser (se não existir)
# ------------------------------------------------------------
echo "👤 Criando superuser padrão (se não existir)..."

python manage.py shell --settings=plantao_pro.settings.dev << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()

username = "05356145438"
email = "admin@example.com"
password = "admin34587895"

u = User.objects.filter(username=username).first()
if not u:
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✔️ Superuser criado:", username)
else:
    print("ℹ️ Superuser já existe:", username)
EOF

echo ""

# ------------------------------------------------------------
# 3) Collectstatic
# ------------------------------------------------------------
echo "📁 Executando collectstatic..."
python manage.py collectstatic --noinput --settings=plantao_pro.settings.dev || true
echo "✔️ Static coletado!"
echo ""

# ------------------------------------------------------------
# 4) Start Django (DEV)
# ------------------------------------------------------------
echo "🚀 Iniciando Django (modo DEV)..."
exec python manage.py runserver 0.0.0.0:8000 --settings=plantao_pro.settings.dev
