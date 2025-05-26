import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    KNOWLEDGE_BASE_PATH = os.getenv("KNOWLEDGE_BASE_PATH", "knowledge.json")

settings = Settings()
