from sqlmodel import Session, select
from app.models.producto import Producto
from app.models.producto_categoria import ProductoCategoria
from app.models.producto_ingrediente import ProductoIngrediente


class ProductoRepository:

    def __init__(self, session: Session):
        self.session = session

    # =========================
    # CREATE / ADD
    # =========================
    def crear(self, producto: Producto):
        self.session.add(producto)

    # =========================
    # GET BY ID
    # =========================
    def obtener_por_id(self, producto_id: int):
        return self.session.get(Producto, producto_id)

    # =========================
    # DELETE RELACIONES
    # =========================
    def eliminar_relaciones_categoria(self, producto_id: int):
        self.session.query(ProductoCategoria).filter(
            ProductoCategoria.producto_id == producto_id
        ).delete()

    def eliminar_relaciones_ingrediente(self, producto_id: int):
        self.session.query(ProductoIngrediente).filter(
            ProductoIngrediente.producto_id == producto_id
        ).delete()