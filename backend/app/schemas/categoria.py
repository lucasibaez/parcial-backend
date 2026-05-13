from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# =========================
# CREATE
# =========================
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None


# =========================
# UPDATE
# =========================
class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None


# =========================
# READ SIMPLE
# =========================
class CategoriaSimple(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


# =========================
# READ TREE
# =========================
class CategoriaTree(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    parent_id: Optional[int] = None

    subcategorias: list["CategoriaTree"] = []

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# =========================
# READ NORMAL
# =========================
class CategoriaRead(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]
    parent_id: Optional[int]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


CategoriaTree.model_rebuild()