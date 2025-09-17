# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y curl && pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app
COPY ./ui /app/ui
COPY ./output /app/output

EXPOSE 8000

# This CMD is designed to run the server in the foreground
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]