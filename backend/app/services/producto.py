from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.core.unit_of_work import UnitOfWork

from app.models.producto import Producto
from app.models.categoria import Categoria
from app.models.ingrediente import Ingrediente
from app.models.producto_categoria import ProductoCategoria
from app.models.producto_ingrediente import ProductoIngrediente

from app.repositorios.producto_repository import ProductoRepository


# =========================================================
# GET ALL
# =========================================================
def listar_productos_service(session: Session, nombre=None, disponible=None, offset=0, limit=10):

    statement = (
        select(Producto)
        .options(
            selectinload(Producto.categorias),
            selectinload(Producto.ingredientes)
        )
        .where(Producto.deleted_at == None)
    )

    if nombre:
        statement = statement.where(Producto.nombre.contains(nombre))

    if disponible is not None:
        statement = statement.where(Producto.disponible == disponible)

    total = len(session.exec(statement).all())

    statement = statement.offset(offset).limit(limit)

    productos = session.exec(statement).all()

    for p in productos:
        p.categorias = [c for c in p.categorias if c.deleted_at is None]
        p.ingredientes = [i for i in p.ingredientes if i.deleted_at is None]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": productos
    }


# =========================================================
# GET BY ID
# =========================================================
def obtener_producto_service(
    session: Session,
    producto_id: int,
    incluir_relaciones: bool = True
):

    statement = select(Producto).where(
        Producto.id == producto_id,
        Producto.deleted_at == None
    )

    # =========================================================
    # RELACIONES OPCIONALES
    # =========================================================
    if incluir_relaciones:
        statement = statement.options(
            selectinload(Producto.categorias),
            selectinload(Producto.ingredientes)
        )

    producto = session.exec(statement).first()

    if not producto:
        raise HTTPException(404, "Producto no encontrado")

    # =========================================================
    # LIMPIEZA RELACIONES
    # =========================================================
    if incluir_relaciones:

        producto.categorias = [
            c for c in producto.categorias
            if c.deleted_at is None
        ]

        producto.ingredientes = [
            i for i in producto.ingredientes
            if i.deleted_at is None
        ]

    else:

        producto.categorias = []
        producto.ingredientes = []

    return producto

# =========================================================
# CREATE
# =========================================================
def crear_producto_service(session: Session, data, validar_relaciones=True):

    try:

        repo = ProductoRepository(session)

        with UnitOfWork(session):

            producto = Producto(
                nombre=data.nombre,
                descripcion=data.descripcion,
                precio_base=data.precio_base,
                imagenes_url=data.imagenes_url,
                disponible=data.disponible,
                stock_cantidad=data.stock_cantidad,
            )

            repo.crear(producto)
            session.flush()

            for cat in data.categorias:

                if validar_relaciones:
                    c = session.get(Categoria, cat.id)
                    if not c or c.deleted_at:
                        raise HTTPException(404, f"Categoria {cat.id}")

                session.add(
                    ProductoCategoria(
                        producto_id=producto.id,
                        categoria_id=cat.id,
                        es_principal=cat.es_principal
                    )
                )

            for ing in data.ingredientes:

                if validar_relaciones:
                    i = session.get(Ingrediente, ing.id)
                    if not i or i.deleted_at:
                        raise HTTPException(404, f"Ingrediente {ing.id}")

                session.add(
                    ProductoIngrediente(
                        producto_id=producto.id,
                        ingrediente_id=ing.id,
                        es_removible=ing.es_removible
                    )
                )

        return obtener_producto_service(session, producto.id)

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(500, "Error creando producto")


# =========================================================
# UPDATE
# =========================================================
def actualizar_producto_service(session: Session, producto_id: int, data):

    try:

        repo = ProductoRepository(session)

        producto = repo.obtener_por_id(producto_id)

        if not producto or producto.deleted_at:
            raise HTTPException(404, "Producto no encontrado")

        with UnitOfWork(session):

            if data.nombre is not None:
                producto.nombre = data.nombre

            if data.descripcion is not None:
                producto.descripcion = data.descripcion

            if data.precio_base is not None:
                producto.precio_base = data.precio_base

            if data.imagenes_url is not None:
                producto.imagenes_url = data.imagenes_url

            if data.disponible is not None:
                producto.disponible = data.disponible

            if data.stock_cantidad is not None:
                producto.stock_cantidad = data.stock_cantidad

            producto.updated_at = datetime.utcnow()

            if data.categorias is not None:

                repo.eliminar_relaciones_categoria(producto_id)

                for cat in data.categorias:

                    c = session.get(Categoria, cat.id)
                    if not c or c.deleted_at:
                        raise HTTPException(404, f"Categoria {cat.id}")

                    session.add(
                        ProductoCategoria(
                            producto_id=producto.id,
                            categoria_id=cat.id,
                            es_principal=cat.es_principal
                        )
                    )

            if data.ingredientes is not None:

                repo.eliminar_relaciones_ingrediente(producto_id)

                for ing in data.ingredientes:

                    i = session.get(Ingrediente, ing.id)
                    if not i or i.deleted_at:
                        raise HTTPException(404, f"Ingrediente {ing.id}")

                    session.add(
                        ProductoIngrediente(
                            producto_id=producto.id,
                            ingrediente_id=ing.id,
                            es_removible=ing.es_removible
                        )
                    )

            session.add(producto)
            session.flush()

        return obtener_producto_service(session, producto.id)

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(500, str(e))


# =========================================================
# DELETE (SOFT)
# =========================================================
def eliminar_producto_service(session: Session, producto_id: int):

    try:

        producto = session.get(Producto, producto_id)

        if not producto or producto.deleted_at:
            raise HTTPException(404, "Producto no encontrado")

        with UnitOfWork(session):

            producto.deleted_at = datetime.utcnow()
            producto.disponible = False
            producto.updated_at = datetime.utcnow()

            session.add(producto)

        return {"ok": True}

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(500, "Error eliminando producto")


# =========================================================
# RESTORE
# =========================================================
def restaurar_producto_service(session: Session, producto_id: int):

    try:

        producto = session.get(Producto, producto_id)

        if not producto or not producto.deleted_at:
            raise HTTPException(404, "Producto no eliminado")

        with UnitOfWork(session):

            producto.deleted_at = None
            producto.disponible = True
            producto.updated_at = datetime.utcnow()

            session.add(producto)

        return obtener_producto_service(session, producto_id)

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(500, "Error restaurando producto")