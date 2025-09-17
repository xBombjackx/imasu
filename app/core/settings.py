# app/core/settings.py
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings."""

    # A1111 API endpoint
    A1111_API_ENDPOINT: str = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    # Ollama model to use for the agent
    OLLAMA_MODEL: str = "llama3.1:8b"
    # Directory to save the generated images
    OUTPUT_DIR: str = "output"

    # Corrected Ollama URL
    OLLAMA_URL: str = "http://imasu_ollama:11434"

    # --- FAST MODE CONFIGURATION ---
    # Set to True to generate multiple low-quality images for faster testing.
    # Set to False for standard high-quality, multi-image generation.
    FAST_MODE: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single settings instance to be used across the application
settings = Settings()

# Ensure the output directory exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
