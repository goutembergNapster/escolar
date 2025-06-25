#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

echo "Esperando o PostgreSQL iniciar..."
sh /scripts/wait_psql.sh

echo "Coletando arquivos estáticos..."
sh /scripts/collectstatic.sh

echo "Rodando migrações..."
sh /scripts/makemigrations.sh
sh /scripts/migrate.sh

echo "Iniciando o servidor Django..."
sh /scripts/runserver.sh
