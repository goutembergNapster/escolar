#!/bin/sh

echo "Aguardando o banco de dados PostgreSQL..."

while ! nc -z psql 5432; do
  sleep 1
done

echo "PostgreSQL iniciado com sucesso."


