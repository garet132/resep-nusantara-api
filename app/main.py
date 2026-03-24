from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import recipes, categories, favorites

# Buat tabel database (hanya pertama kali)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resep Nusantara API",
    description="API untuk aplikasi resep masakan nusantara",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware - agar bisa diakses dari aplikasi Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, di production ganti dengan domain spesifik
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(recipes.router)
app.include_router(categories.router)
app.include_router(favorites.router)

@app.get("/")
def root():
    return {
        "message": "Selamat datang di API Resep Nusantara",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}