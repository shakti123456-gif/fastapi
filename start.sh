#!/bin/bash

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# Run the Uvicorn server with 4 workers
uvicorn main:app --host 0.0.0.0 --workers 4