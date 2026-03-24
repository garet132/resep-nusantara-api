import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Deteksi environment (apakah di cloud atau lokal)
IS_CLOUD = os.environ.get('LEAPCELL_ENV') or os.environ.get('RENDER')

if IS_CLOUD:
    # Di Leapcell/Render, gunakan folder /tmp
    DB_PATH = '/tmp/resep_nusantara.db'
else:
    # Di lokal, gunakan folder proyek
    DB_PATH = './resep_nusantara.db'

DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"📁 Database path: {DB_PATH}")  # Untuk debugging

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()