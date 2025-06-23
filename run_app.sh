#!/bin/bash

APP_NAME="smart-supply-backend"
CONTAINER_NAME="smart-supply-backend-container"

# Ensure .env file exists
if [ ! -f ".env" ]; then
  echo "[INFO] .env file not found. Copying from .env.example..."
  cp .env.example .env
fi

if [ "$1" == "docker" ]; then
  echo "[INFO] Running in Docker mode..."
  # Stop and remove existing container if running
  if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "[INFO] Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
  fi
  # Remove old image
  if [ $(docker images -q $APP_NAME) ]; then
    echo "[INFO] Removing old Docker image..."
    docker rmi $APP_NAME
  fi
  # Build new image
  echo "[INFO] Building Docker image..."
  docker build -t $APP_NAME .
  # Run container
  echo "[INFO] Running Docker container..."
  docker run --env-file .env -p 8000:8000 --name $CONTAINER_NAME $APP_NAME
else
  echo "[INFO] Running locally with Uvicorn..."
  # Set up Python virtual environment if not already present
  if [ ! -d ".venv" ]; then
    python3 -m venv .venv
  fi
  # Activate the virtual environment
  source .venv/bin/activate
  # Install dependencies
  pip install --upgrade pip
  pip install -r requirements.txt
  uvicorn main:app --reload
fi 