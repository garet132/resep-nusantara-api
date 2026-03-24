from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Resep(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    judul = Column(String(200), nullable=False, index=True)
    deskripsi = Column(Text, nullable=True)
    gambar = Column(String(500), nullable=True)
    waktu_masak = Column(Integer, default=30)  # dalam menit
    tingkat_kesulitan = Column(String(20), default="Mudah")  # Mudah, Sedang, Sulit
    porsi = Column(Integer, default=2)
    kategori = Column(String(50), index=True)
    daerah = Column(String(50), index=True)  # asal daerah (Jawa, Padang, dll)
    instruksi = Column(Text, nullable=False)
    sumber = Column(String(500), nullable=True)  # sumber resep (URL)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relasi dengan bahan (one-to-many)
    bahan_list = relationship("Bahan", back_populates="resep", cascade="all, delete-orphan")
    
    # Relasi dengan favorit (one-to-many)
    favorit_list = relationship("Favorit", back_populates="resep", cascade="all, delete-orphan")


class Bahan(Base):
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    resep_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    nama = Column(String(100), nullable=False)
    ukuran = Column(String(50), nullable=True)  # 2 sdm, 1/2 sdt, dll
    
    resep = relationship("Resep", back_populates="bahan_list")


class Favorit(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    resep_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    user_id = Column(String(50), default="default_user")  # untuk multi-user nanti
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resep = relationship("Resep", back_populates="favorit_list")