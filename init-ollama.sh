#!/bin/sh
set -e

# Start the Ollama server in the background
/bin/ollama serve &

# Capture the process ID
pid=$!

# Wait a few seconds for the server to be ready
echo "Waiting for Ollama server to start..."
sleep 5

# Pull the model
echo "Pulling model: llama3.1:8b"
ollama pull llama3.1:8b
echo "Model pull complete."

# Bring the server process to the foreground
# This will keep the container running
wait $pid