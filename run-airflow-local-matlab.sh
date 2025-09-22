#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Get current UID et GID
export AIRFLOW_UID=$(id -u)
export AIRFLOW_GID=$(id -g)

export MATLAB_RUN_DIR="${1:-./to-be-define}"
# Check MATLAB runtime exists
if [[ ! -d "$MATLAB_RUN_DIR" ]]; then
  echo "❌ Directory '$MATLAB_RUN_DIR' does not exists."
  echo "   Call script with attribut : ./run-airflow.sh /absolute-path-to/matlab-runtime"
  exit 1
fi

# Run Airflow with docker compose
echo "🚀 Running d'Airflow using local MATLAB runtime..."
docker compose up -d

echo "ℹ️ See logs : docker compose logs -f"
