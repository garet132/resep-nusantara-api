from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.sql.expression import or_
from . import models, schemas
from typing import List, Optional

# ========== CRUD Resep ==========

def get_resep(db: Session, resep_id: int):
    """Ambil resep berdasarkan ID"""
    return db.query(models.Resep).filter(models.Resep.id == resep_id).first()

def get_resep_all(db: Session, skip: int = 0, limit: int = 100):
    """Ambil semua resep dengan pagination"""
    return db.query(models.Resep).offset(skip).limit(limit).all()

def get_resep_random(db: Session, count: int = 5):
    """Ambil resep random"""
    return db.query(models.Resep).order_by(func.random()).limit(count).all()

def search_resep(db: Session, query: str, skip: int = 0, limit: int = 20):
    """Cari resep berdasarkan judul atau kategori atau daerah"""
    return db.query(models.Resep).filter(
        or_(
            models.Resep.judul.ilike(f"%{query}%"),
            models.Resep.kategori.ilike(f"%{query}%"),
            models.Resep.daerah.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

def get_resep_by_category(db: Session, category: str, skip: int = 0, limit: int = 20):
    """Filter resep berdasarkan kategori"""
    return db.query(models.Resep).filter(
        models.Resep.kategori.ilike(f"%{category}%")
    ).offset(skip).limit(limit).all()

def get_resep_by_area(db: Session, area: str, skip: int = 0, limit: int = 20):
    """Filter resep berdasarkan daerah"""
    return db.query(models.Resep).filter(
        models.Resep.daerah.ilike(f"%{area}%")
    ).offset(skip).limit(limit).all()

def create_resep(db: Session, resep: schemas.ResepCreate):
    """Buat resep baru beserta bahan-bahannya"""
    # Buat resep utama
    db_resep = models.Resep(
        judul=resep.judul,
        deskripsi=resep.deskripsi,
        gambar=resep.gambar,
        waktu_masak=resep.waktu_masak,
        tingkat_kesulitan=resep.tingkat_kesulitan,
        porsi=resep.porsi,
        kategori=resep.kategori,
        daerah=resep.daerah,
        instruksi=resep.instruksi,
        sumber=resep.sumber
    )
    db.add(db_resep)
    db.flush()  # Dapatkan id tanpa commit
    
    # Buat bahan-bahan
    for bahan in resep.bahan_list:
        db_bahan = models.Bahan(
            resep_id=db_resep.id,
            nama=bahan.nama,
            ukuran=bahan.ukuran
        )
        db.add(db_bahan)
    
    db.commit()
    db.refresh(db_resep)
    return db_resep

def update_resep(db: Session, resep_id: int, resep_update: schemas.ResepUpdate):
    """Update resep yang sudah ada"""
    db_resep = get_resep(db, resep_id)
    if not db_resep:
        return None
    
    update_data = resep_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_resep, field, value)
    
    db.commit()
    db.refresh(db_resep)
    return db_resep

def delete_resep(db: Session, resep_id: int):
    """Hapus resep (bahan akan otomatis terhapus karena cascade)"""
    db_resep = get_resep(db, resep_id)
    if not db_resep:
        return None
    
    db.delete(db_resep)
    db.commit()
    return db_resep


# ========== CRUD Kategori ==========

def get_all_categories(db: Session):
    """Ambil semua kategori unik"""
    categories = db.query(models.Resep.kategori).distinct().all()
    return [c[0] for c in categories if c[0]]


# ========== CRUD Favorit ==========

def get_favorites(db: Session, user_id: str = "default_user"):
    """Ambil semua resep favorit user"""
    favorites = db.query(models.Favorit).filter(
        models.Favorit.user_id == user_id
    ).all()
    return [fav.resep for fav in favorites]

def add_favorite(db: Session, resep_id: int, user_id: str = "default_user"):
    """Tambah resep ke favorit"""
    # Cek apakah sudah ada
    existing = db.query(models.Favorit).filter(
        models.Favorit.resep_id == resep_id,
        models.Favorit.user_id == user_id
    ).first()
    
    if existing:
        return existing
    
    db_favorite = models.Favorit(resep_id=resep_id, user_id=user_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def remove_favorite(db: Session, resep_id: int, user_id: str = "default_user"):
    """Hapus resep dari favorit"""
    db_favorite = db.query(models.Favorit).filter(
        models.Favorit.resep_id == resep_id,
        models.Favorit.user_id == user_id
    ).first()
    
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
        return True
    return False

def is_favorite(db: Session, resep_id: int, user_id: str = "default_user"):
    """Cek apakah resep favorit"""
    return db.query(models.Favorit).filter(
        models.Favorit.resep_id == resep_id,
        models.Favorit.user_id == user_id
    ).first() is not None