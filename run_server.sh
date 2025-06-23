#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload 