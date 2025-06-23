#!/bin/bash

# Set up Python virtual environment if not already present
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Ensure .env file exists
if [ ! -f ".env" ]; then
  echo "[INFO] .env file not found. Copying from .env.example..."
  cp .env.example .env
fi

# Run the FastAPI server
uvicorn main:app --reload 