#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "🐳 Building and starting services (db, backend, frontend)..."
docker compose up -d --build db backend frontend

echo "🌱 Seeding lessons from backend/seed/*.json..."
docker compose exec backend python seed_db.py

cleanup() {
  echo ""
  echo "🛑 Stopping services..."
  docker compose stop backend frontend >/dev/null 2>&1 || true
}
trap cleanup INT TERM

echo "📜 Streaming backend/frontend logs (Ctrl+C to stop)..."
docker compose logs -f backend frontend
