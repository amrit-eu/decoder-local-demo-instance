#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Run Airflow with docker compose
echo "🚀 Stopping d'Airflow..."
docker compose down
