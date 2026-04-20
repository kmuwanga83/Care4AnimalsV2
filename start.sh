#!/bin/bash

# 1. Start the Backend
echo "🚀 Starting FastAPI Backend..."
cd backend
# Attempt to activate virtual environment if it exists
if [ -d "venv" ]; then source venv/Scripts/activate; fi
if [ -d "env" ]; then source env/Scripts/activate; fi

# Run uvicorn (using python -m ensures it finds the installed package)
python -m uvicorn app.main:app --port 8000 --reload & 

# 2. Start the Frontend
echo "💻 Starting Vite Frontend..."
cd ../frontend
# We force port 5173 to keep the 'handshake' consistent
npm run dev -- --port 5173 &

# 3. Wait for processes
wait
