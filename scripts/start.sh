#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Start the FastAPI backend in the background
echo "Starting FastAPI backend..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

# Start the Streamlit UI in the background
echo "Starting Streamlit UI..."
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Function to shut down background processes
shutdown() {
  echo "Shutting down..."
  kill -TERM "$UVICORN_PID" "$STREAMLIT_PID"
  wait "$UVICORN_PID"
  wait "$STREAMLIT_PID"
  echo "Shutdown complete."
}

# Trap signals and call the shutdown function
trap shutdown SIGTERM SIGINT

# Wait for either process to exit
wait -n $UVICORN_PID $STREAMLIT_PID

# If one process exits, shut down the other and exit
shutdown
