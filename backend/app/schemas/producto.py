from pydantic import BaseModel
from typing import List, Optional


# =========================
# CATEGORIA EN PRODUCTO (INPUT)
# =========================
class ProductoCategoriaIn(BaseModel):
    id: int
    es_principal: bool = False


# =========================
# INGREDIENTE EN PRODUCTO (INPUT)
# =========================
class ProductoIngredienteIn(BaseModel):
    id: int
    es_removible: bool = False


# =========================
# CREATE PRODUCTO
# =========================
class ProductoCreate(BaseModel):

    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    stock_cantidad: int
    imagenes_url: Optional[List[str]] = None
    disponible: Optional[bool] = True

    categorias: List[ProductoCategoriaIn] = []
    ingredientes: List[ProductoIngredienteIn] = []


# =========================
# UPDATE PRODUCTO
# =========================
class ProductoUpdate(BaseModel):

    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    stock_cantidad: Optional[int] = None
    imagenes_url: Optional[List[str]] = None
    disponible: Optional[bool] = None

    categorias: Optional[List[ProductoCategoriaIn]] = None
    ingredientes: Optional[List[ProductoIngredienteIn]] = None


# =========================
# CATEGORIA SIMPLE (OUTPUT)
# =========================
class CategoriaSimple(BaseModel):

    id: int
    nombre: str
    parent_id: Optional[int] = None
    es_principal: bool = False

    class Config:
        from_attributes = True


# =========================
# INGREDIENTE SIMPLE (OUTPUT)
# =========================
class IngredienteSimple(BaseModel):

    id: int
    nombre: str
    es_alergeno: bool

    class Config:
        from_attributes = True


# =========================
# READ PRODUCTO
# =========================
class ProductoRead(BaseModel):

    id: int
    nombre: str
    descripcion: Optional[str]

    precio_base: float
    stock_cantidad: int

    imagenes_url: Optional[List[str]] = None
    disponible: Optional[bool] = None

    categorias: List[CategoriaSimple] = []
    ingredientes: List[IngredienteSimple] = []

    class Config:
        from_attributes = True