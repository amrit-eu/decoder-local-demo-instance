#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get current UID et GID
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)
export MATLAB_RUN_DIR="${1:-.}"

# Run Airflow with docker compose
echo "🚫 Stopping d'Airflow..."
docker compose down
