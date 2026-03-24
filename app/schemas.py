from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# ========== Bahan Schemas ==========
class BahanBase(BaseModel):
    nama: str
    ukuran: Optional[str] = None

class BahanCreate(BahanBase):
    pass

class BahanResponse(BahanBase):
    id: int
    resep_id: int
    
    class Config:
        from_attributes = True


# ========== Resep Schemas ==========
class ResepBase(BaseModel):
    judul: str
    deskripsi: Optional[str] = None
    gambar: Optional[str] = None
    waktu_masak: int = 30
    tingkat_kesulitan: str = "Mudah"
    porsi: int = 2
    kategori: Optional[str] = None
    daerah: Optional[str] = None
    instruksi: str
    sumber: Optional[str] = None

class ResepCreate(ResepBase):
    bahan_list: List[BahanCreate] = []  # list bahan saat membuat resep

class ResepUpdate(BaseModel):
    judul: Optional[str] = None
    deskripsi: Optional[str] = None
    gambar: Optional[str] = None
    waktu_masak: Optional[int] = None
    tingkat_kesulitan: Optional[str] = None
    porsi: Optional[int] = None
    kategori: Optional[str] = None
    daerah: Optional[str] = None
    instruksi: Optional[str] = None
    sumber: Optional[str] = None

class ResepResponse(ResepBase):
    id: int
    created_at: datetime
    updated_at: datetime
    bahan_list: List[BahanResponse] = []
    
    class Config:
        from_attributes = True


# ========== Favorit Schemas ==========
class FavoritResponse(BaseModel):
    id: int
    resep_id: int
    resep: ResepResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========== Response Umum ==========
class MessageResponse(BaseModel):
    message: str
    success: bool = True