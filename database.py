from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

# SQLAlchemy bağlantısı
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model class
Base = declarative_base()

# Database session için Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# --- Veritabanı bağlantı testi ---
if __name__ == "__main__":
    try:
        # Veritabanına bağlantı testi (boş bir sorgu)
        with engine.connect() as connection:
            print("✅ Veritabanı bağlantısı başarılı!")
    except Exception as e:
        print("❌ Veritabanına bağlanılamadı!")
        print(e)
