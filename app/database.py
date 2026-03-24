import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Ambil URL database dari environment variable
# Untuk Leapcell, kita akan set ini di dashboard
DATABASE_URL = os.environ.get("DATABASE_URL")

# Jika tidak ada, gunakan SQLite untuk development lokal
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./resep_nusantara.db"
    print("⚠️ Using SQLite (development mode)")
else:
    print(f"✅ Using PostgreSQL: {DATABASE_URL[:30]}...")  # Hanya tampilkan awal untuk keamanan

# Engine untuk PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Sesuaikan dengan kebutuhan
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()