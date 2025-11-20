#!/usr/bin/env bash
set -e

URL="$1"

if [ -z "$URL" ]; then
  echo "[wait_psql] DATABASE_URL vazio — seguindo sem esperar."
  exit 0
fi

echo "[wait_psql] URL recebida: $URL"

# ============================================================
# 📌 Extração robusta da URL (funciona com qualquer Postgres://)
# ============================================================

# remove o prefixo (postgres://)
proto="$(echo $URL | sed -e's,^\(.*://\).*,\1,g')"
url_no_proto="${URL/$proto/}"

# separa user:pass  e host:port/db
userpass="$(echo $url_no_proto | cut -d@ -f1)"
hostportdb="$(echo $url_no_proto | cut -d@ -f2)"

USER="$(echo $userpass | cut -d: -f1)"
PASSWORD="$(echo $userpass | cut -d: -f2)"

HOST="$(echo $hostportdb | cut -d: -f1)"
PORT="$(echo $hostportdb | cut -d: -f2 | cut -d/ -f1)"

# =========================================
# 🔄 FALLBACK se algum campo vier vazio
# =========================================
[ -z "$USER" ] && USER="admin"
[ -z "$PASSWORD" ] && PASSWORD=""
[ -z "$HOST" ] && HOST="db"
[[ ! "$PORT" =~ ^[0-9]+$ ]] && PORT=5432

echo "[wait_psql] Conectando com:"
echo "  USER=$USER"
echo "  PASS=${PASSWORD:-<vazio>}"
echo "  HOST=$HOST"
echo "  PORT=$PORT"
echo ""

# ============================================================
# 🕒 LOOP DE TENTATIVAS (90 tentativas, 2s cada)
# ============================================================

for i in $(seq 1 90); do
  if PGPASSWORD="$PASSWORD" pg_isready -h "$HOST" -p "$PORT" -U "$USER" >/dev/null 2>&1; then
    echo "[wait_psql] ✅ Postgres pronto!"
    exit 0
  fi

  echo "[wait_psql] Tentativa $i/90..."
  sleep 2
done

echo "[wait_psql] ❌ Timeout ao esperar Postgres."
exit 1
