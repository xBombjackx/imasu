from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # ✅ Ensures it loads A1111_URL from .env
    A1111_URL: str = "http://127.0.0.1:7860"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OUTPUT_DIR: str = "output"
    # ✅ Ensures it uses the correct 'ollama' service name
    OLLAMA_URL: str = "http://ollama:11434"
    FAST_MODE: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
# Ensure the output directory exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
