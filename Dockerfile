# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install curl for health checks and bash for the start script
RUN apt-get update && apt-get install -y curl bash

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app ./app
COPY ./ui ./ui
COPY ./scripts/start.sh ./scripts/

# Make the start script executable
RUN chmod +x ./scripts/start.sh

# Expose the ports the app runs on
EXPOSE 8000
EXPOSE 8501

# Run the startup script
CMD ["./scripts/start.sh"]