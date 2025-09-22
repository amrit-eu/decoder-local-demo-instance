#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get current UID et GID
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)

# Run Airflow with docker compose
echo "🚀 Running d'Airflow..."
docker compose up -d

echo "ℹ️ See logs : docker compose logs -f"
