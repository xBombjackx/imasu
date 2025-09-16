import os

# The URL for the AUTOMATIC1111 API
# It will use the environment variable from Docker Compose, or default to localhost
A1111_URL = os.getenv("A1111_URL", "http://localhost:7860")

# The directory to save generated images
OUTPUT_DIR = "output"
