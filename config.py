import os
from dotenv import load_dotenv

load_dotenv()

RETENTION_HOURS = int(os.getenv("RETENTION_HOURS", "24"))
BACKGROUND_TIMEOUT_SECONDS = float(os.getenv("BACKGROUND_TIMEOUT_SECONDS", "30"))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "storage/uploads")
LOG_FILE = os.getenv("LOG_FILE", "storage/audit.log")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_FILE_MB = int(os.getenv("MAX_FILE_MB", "15"))
