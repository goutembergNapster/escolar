#!/bin/bash

# Nome do banco e usuário
DB_NAME="escolinha_db"
DB_USER="admin"

echo "🔁 Parando containers..."
docker-compose down -v

echo "🧹 Limpando arquivos de migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "🧹 Removendo possível banco SQLite..."
rm -f db.sqlite3

echo "🚀 Subindo containers novamente..."
docker-compose up -d --build

echo "⏳ Aguardando PostgreSQL iniciar..."
sleep 5

echo "🗑️ Apagando banco antigo (se existir)..."
docker exec -it psql psql -U $DB_USER -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DB_NAME';"
docker exec -it psql psql -U $DB_USER -d postgres -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker exec -it psql psql -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME WITH OWNER = $DB_USER ENCODING 'UTF8';"

echo "✅ Banco $DB_NAME recriado."

echo "📦 Rodando migrations..."
docker exec -e DJANGO_SETTINGS_MODULE=plantao_pro.settings -it escolinha python manage.py makemigrations
docker exec -e DJANGO_SETTINGS_MODULE=plantao_pro.settings -it escolinha python manage.py migrate

echo "👤 Criando superusuário 'goutemberg' com senha '34587895'..."
docker exec -e DJANGO_SETTINGS_MODULE=plantao_pro.settings -it escolinha python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='goutemberg').exists():
    User.objects.create_superuser(username='goutemberg', password='34587895', email='admin@example.com');
"

echo "✅ Reset completo concluído com sucesso!"