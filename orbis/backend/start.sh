#!/bin/bash
# Start the ORBIS backend
# Usage: ./start.sh
# Requires: backend/.env with ANTHROPIC_API_KEY=sk-ant-...

cd "$(dirname "$0")"

if [ ! -f .env ]; then
  echo "ERROR: .env file missing. Copy .env.example and add your ANTHROPIC_API_KEY."
  exit 1
fi

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
