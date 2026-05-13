from sqlmodel import Session, select

from app.models.ingrediente import Ingrediente
from app.models.producto_ingrediente import ProductoIngrediente


class IngredienteRepository:

    def __init__(self, session: Session):
        self.session = session

    # =========================================================
    # CREATE
    # =========================================================
    def crear(self, ingrediente: Ingrediente):
        self.session.add(ingrediente)

    # =========================================================
    # GET BY ID
    # =========================================================
    def obtener_por_id(self, ingrediente_id: int):
        return self.session.get(Ingrediente, ingrediente_id)

    # =========================================================
    # LISTAR
    # =========================================================
    def listar(
        self,
        nombre=None,
        es_alergeno=None,
        offset: int = 0,
        limit: int = 10
    ):

        statement = (
            select(Ingrediente)
            .where(Ingrediente.deleted_at == None)
        )

        if nombre:
            statement = statement.where(
                Ingrediente.nombre.contains(nombre)
            )

        if es_alergeno is not None:
            statement = statement.where(
                Ingrediente.es_alergeno == es_alergeno
            )

        statement = statement.offset(offset).limit(limit)

        return self.session.exec(statement).all()

    # =========================================================
    # DELETE RELACIONES PRODUCTO-INGREDIENTE
    # =========================================================
    def eliminar_relaciones_producto(self, ingrediente_id: int):

        self.session.query(ProductoIngrediente).filter(
            ProductoIngrediente.ingrediente_id == ingrediente_id
        ).delete()