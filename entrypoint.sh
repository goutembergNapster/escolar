#!/bin/bash
set -e

echo "Rodando migrações..."
python manage.py migrate --noinput --settings=plantao_pro.settings.prod

echo "Limpando staticfiles antigo..."
rm -rf /app/staticfiles/*
rm -f /app/staticfiles/staticfiles.json

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --settings=plantao_pro.settings.prod

echo "Criando superusuário padrão (se não existir)..."
python - << 'EOF'
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

username = "goutemberg"
email = "goutemberg@icloud.com"
password = "Gps34587895@&*"

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print("Superusuário criado com sucesso.")
    else:
        print("Superusuário já existe, ignorando.")
except IntegrityError as e:
    print("Erro ao criar superusuário:", e)
EOF

echo "Iniciando servidor..."
exec "$@"
