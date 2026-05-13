from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.models.producto_categoria import ProductoCategoria


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

    # RELACIÓN REFLEXIVA
    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="categoria.id"
    )

    parent: Optional["Categoria"] = Relationship(
        back_populates="subcategorias",
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )

    subcategorias: List["Categoria"] = Relationship(
        back_populates="parent"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    productos: List["Producto"] = Relationship(
        back_populates="categorias",
        link_model=ProductoCategoria
    )


from app.models.producto import Producto