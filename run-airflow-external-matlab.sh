#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get current UID et GID
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)

echo "🚀 Running Airflow using 'MATLAB container'…"
docker compose --profile default --profile matlab up -d

echo
echo "ℹ️ See logs :"
echo "   docker compose --profile default --profile matlab -f logs -f"
echo
echo "✅ Access Airflow (default) : http://localhost:8080"
