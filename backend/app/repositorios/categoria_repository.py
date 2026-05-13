# =========================================================
# categoria_repository.py
# =========================================================

from sqlmodel import Session, select
from app.models.categoria import Categoria
from app.models.producto_categoria import ProductoCategoria


class CategoriaRepository:

    def __init__(self, session: Session):
        self.session = session

    # =========================================================
    # CREATE
    # =========================================================
    def crear(self, categoria: Categoria):
        self.session.add(categoria)

    # =========================================================
    # GET BY ID
    # =========================================================
    def obtener_por_id(self, categoria_id: int):
        return self.session.get(Categoria, categoria_id)

    # =========================================================
    # LISTAR
    # =========================================================
    def listar(
        self,
        nombre=None,
        offset: int = 0,
        limit: int = 10
    ):

        statement = (
            select(Categoria)
            .where(Categoria.deleted_at == None)
        )

        if nombre:
            statement = statement.where(
                Categoria.nombre.contains(nombre)
            )

        statement = statement.offset(offset).limit(limit)

        return self.session.exec(statement).all()

    # =========================================================
    # DELETE RELACIONES PRODUCTO-CATEGORIA
    # =========================================================
    def eliminar_relaciones_producto(self, categoria_id: int):

        self.session.query(ProductoCategoria).filter(
            ProductoCategoria.categoria_id == categoria_id
        ).delete()