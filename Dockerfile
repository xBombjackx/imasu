# Use an official Python runtime as a parent image
FROM python:3.11-slim

# --- ADD THIS LINE ---
# Install curl, which is needed for the health check in docker-compose
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./app /app/app
COPY ./ui /app/ui

# Expose the ports the app runs on
EXPOSE 8000
EXPOSE 8501

# Create a simple script to start both services
CMD ["/bin/bash", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0"]