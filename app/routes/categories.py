from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[str])
def get_categories(
    db: Session = Depends(get_db)
):
    """Mendapatkan semua kategori resep"""
    return crud.get_all_categories(db)