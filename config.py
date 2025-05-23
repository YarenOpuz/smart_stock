import os
from dotenv import load_dotenv
from pathlib import Path

# .env dosyasını yükle
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Veritabanı ayarları
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/smart_stock")

# API ayarları
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() in ('true', '1', 't')

# JWT ayarları
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")) 