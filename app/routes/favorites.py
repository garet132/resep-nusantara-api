from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/", response_model=List[schemas.ResepResponse])
def get_favorites(
    user_id: str = Query("default_user", description="ID pengguna"),
    db: Session = Depends(get_db)
):
    """Mendapatkan semua resep favorit pengguna"""
    return crud.get_favorites(db, user_id=user_id)

@router.post("/{resep_id}", response_model=schemas.MessageResponse)
def add_favorite(
    resep_id: int,
    user_id: str = Query("default_user"),
    db: Session = Depends(get_db)
):
    """Menambahkan resep ke favorit"""
    # Cek apakah resep ada
    resep = crud.get_resep(db, resep_id)
    if not resep:
        raise HTTPException(status_code=404, detail="Resep tidak ditemukan")
    
    crud.add_favorite(db, resep_id, user_id)
    return {"message": "Resep ditambahkan ke favorit", "success": True}

@router.delete("/{resep_id}", response_model=schemas.MessageResponse)
def remove_favorite(
    resep_id: int,
    user_id: str = Query("default_user"),
    db: Session = Depends(get_db)
):
    """Menghapus resep dari favorit"""
    removed = crud.remove_favorite(db, resep_id, user_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Resep tidak ada di favorit")
    return {"message": "Resep dihapus dari favorit", "success": True}