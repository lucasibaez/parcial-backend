from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db import engine

# IMPORTA MODELOS (esto registra metadata)
import app.models

# ROUTES
from app.routes.producto import router as producto_router
from app.routes.categoria import router as categoria_router
from app.routes.ingrediente import router as ingrediente_router


app = FastAPI(
    title="Parcial API",
    version="1.0.0"
)


# =========================
# CREACIÓN DE TABLAS
# =========================
@app.on_event("startup")
def on_startup():
    print("🚀 Creando tablas si no existen...")
    SQLModel.metadata.create_all(engine)


# =========================
# ROUTES
# =========================
app.include_router(producto_router)
app.include_router(categoria_router)
app.include_router(ingrediente_router)


# =========================
# HEALTHCHECK
# =========================
@app.get("/")
def root():
    return {"status": "ok"}