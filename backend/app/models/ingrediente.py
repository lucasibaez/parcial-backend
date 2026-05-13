from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.models.producto_ingrediente import ProductoIngrediente


class Ingrediente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str
    descripcion: Optional[str] = None
    es_alergeno: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None  # ← AGREGAR ESTO

    productos: List["Producto"] = Relationship(
        back_populates="ingredientes",
        link_model=ProductoIngrediente
    )


from app.models.producto import Producto