from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ProductoIngrediente(SQLModel, table=True):
    producto_id: Optional[int] = Field(
        default=None, foreign_key="producto.id", primary_key=True
    )
    ingrediente_id: Optional[int] = Field(
        default=None, foreign_key="ingrediente.id", primary_key=True
    )
    es_removible: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)