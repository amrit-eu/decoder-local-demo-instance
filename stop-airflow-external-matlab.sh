#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get current UID et GID
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)

# Run Airflow with docker compose
echo "🚫 Stopping d'Airflow..."
docker compose --profile default --profile matlab down
