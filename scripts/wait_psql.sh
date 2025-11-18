#!/usr/bin/env bash
set -e

URL="$1"
if [ -z "$URL" ]; then
  echo "[wait_psql] DATABASE_URL vazio — seguindo assim mesmo."
  exit 0
fi

# Extrai user, host e port da DATABASE_URL
USER=$(echo "$URL" | sed -E 's|.*//([^:]+):.*|\1|')
HOST=$(echo "$URL" | sed -E 's|.*@([^:/]+).*|\1|')
PORT=$(echo "$URL" | sed -E 's|.*:([0-9]+)/.*|\1|')

# fallback se parsing falhar
[ -z "$USER" ] && USER="admin"
[ -z "$HOST" ] && HOST="db"
if ! echo "$PORT" | grep -Eq '^[0-9]+$'; then
  PORT=5432
fi

echo "[wait_psql] Aguardando Postgres em ${HOST}:${PORT} usando usuário ${USER}..."

for i in $(seq 1 60); do
  if PGPASSWORD="" pg_isready -h "$HOST" -p "$PORT" -U "$USER" >/dev/null 2>&1; then
    echo "[wait_psql] Postgres pronto!"
    exit 0
  fi
  sleep 1
done

echo "[wait_psql] ❌ Timeout ao esperar Postgres."
exit 1
