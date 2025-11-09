#!/bin/bash

echo "🚀 Starting MicroServices..."

# ---------- Virtual environment ----------
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "✅ Virtual environment activated"
else
  echo "⚠️ No virtual environment found."
  echo "👉 Run the following first:"
  echo "python3.12 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# ---------- Initialize SQLite database ----------
DB_DIR="db"
DB_FILE="$DB_DIR/app.sqlite3"
SCHEMA_FILE="$DB_DIR/schema.sql"
SEED_FILE="$DB_DIR/seed.sql"

echo "🧱 Initializing local SQLite database..."

# Ensure db folder exists
mkdir -p "$DB_DIR"

# Check for SQLite CLI
if ! command -v sqlite3 &> /dev/null
then
    echo "❌ sqlite3 command not found. Please install SQLite:"
    echo "   macOS: brew install sqlite"
    echo "   Ubuntu: sudo apt install sqlite3"
    echo "   Windows: ensure sqlite3.exe is in PATH"
    exit 1
fi

# Create schema if missing
if [ -f "$SCHEMA_FILE" ]; then
  sqlite3 "$DB_FILE" < "$SCHEMA_FILE"
  echo "✅ Schema applied"
else
  echo "⚠️ schema.sql not found in $DB_DIR — skipping"
fi

# Load seed data if available
if [ -f "$SEED_FILE" ]; then
  sqlite3 "$DB_FILE" < "$SEED_FILE"
  echo "✅ Seed data loaded"
else
  echo "⚠️ seed.sql not found in $DB_DIR — skipping seed load"
fi

# ---------- Start microservices ----------
echo "🚀 Launching FastAPI services..."

# Search & Filter Service
echo "Starting Search & Filter Service on port 8003..."
uvicorn main:app --app-dir search_filter_service --port 8003 --reload &

# Task Completion Service
echo "Starting Task Completion Service on port 8004..."
uvicorn main:app --app-dir taskcompletion_service --port 8004 --reload &

echo ""
echo "✅ Both services are now running!"
echo "→ Search & Filter Swagger: http://127.0.0.1:8003/docs"
echo "→ Task Completion Swagger: http://127.0.0.1:8004/docs"
echo ""
echo "🧩 Database file: $DB_FILE"
echo "📦 Schema: $SCHEMA_FILE"
echo "🌱 Seed: $SEED_FILE"
echo ""
echo "Press Ctrl + C to stop all services."

# Keep processes alive
wait
