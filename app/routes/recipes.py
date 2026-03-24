from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/", response_model=List[schemas.ResepResponse])
def read_recipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Mendapatkan semua resep"""
    recipes = crud.get_resep_all(db, skip=skip, limit=limit)
    return recipes

@router.get("/random", response_model=List[schemas.ResepResponse])
def read_random_recipes(
    count: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """Mendapatkan resep random"""
    recipes = crud.get_resep_random(db, count=count)
    return recipes

@router.get("/search", response_model=List[schemas.ResepResponse])
def search_recipes(
    q: str = Query(..., min_length=1, description="Keyword pencarian"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Mencari resep berdasarkan judul, kategori, atau daerah"""
    recipes = crud.search_resep(db, query=q, skip=skip, limit=limit)
    return recipes

@router.get("/category/{category}", response_model=List[schemas.ResepResponse])
def filter_by_category(
    category: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Filter resep berdasarkan kategori"""
    recipes = crud.get_resep_by_category(db, category=category, skip=skip, limit=limit)
    return recipes

@router.get("/area/{area}", response_model=List[schemas.ResepResponse])
def filter_by_area(
    area: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Filter resep berdasarkan daerah asal"""
    recipes = crud.get_resep_by_area(db, area=area, skip=skip, limit=limit)
    return recipes

@router.get("/{resep_id}", response_model=schemas.ResepResponse)
def read_recipe(
    resep_id: int,
    db: Session = Depends(get_db)
):
    """Mendapatkan detail resep berdasarkan ID"""
    recipe = crud.get_resep(db, resep_id=resep_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Resep tidak ditemukan")
    return recipe

@router.post("/", response_model=schemas.ResepResponse, status_code=201)
def create_recipe(
    recipe: schemas.ResepCreate,
    db: Session = Depends(get_db)
):
    """Membuat resep baru"""
    return crud.create_resep(db, recipe)

@router.put("/{resep_id}", response_model=schemas.ResepResponse)
def update_recipe(
    resep_id: int,
    recipe_update: schemas.ResepUpdate,
    db: Session = Depends(get_db)
):
    """Mengupdate resep yang sudah ada"""
    recipe = crud.update_resep(db, resep_id, recipe_update)
    if not recipe:
        raise HTTPException(status_code=404, detail="Resep tidak ditemukan")
    return recipe

@router.delete("/{resep_id}", response_model=schemas.MessageResponse)
def delete_recipe(
    resep_id: int,
    db: Session = Depends(get_db)
):
    """Menghapus resep"""
    recipe = crud.delete_resep(db, resep_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Resep tidak ditemukan")
    return {"message": "Resep berhasil dihapus", "success": True}