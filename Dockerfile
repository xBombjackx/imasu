# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app ./app

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]