from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session

from app.core.unit_of_work import UnitOfWork

from app.models.categoria import Categoria
from app.models.producto_categoria import ProductoCategoria

from app.repositorios.categoria_repository import CategoriaRepository

from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaUpdate
)


# =========================================================
# CREATE
# =========================================================
def crear_categoria_service(session: Session, data: CategoriaCreate):

    try:

        repo = CategoriaRepository(session)

        # VALIDAR CATEGORÍA PADRE
        if data.parent_id is not None:

            parent = repo.obtener_por_id(data.parent_id)

            if not parent or parent.deleted_at is not None:
                raise HTTPException(
                    status_code=404,
                    detail="Categoría padre no encontrada"
                )

        with UnitOfWork(session):

            categoria = Categoria(
                nombre=data.nombre,
                descripcion=data.descripcion,
                imagen_url=data.imagen_url,
                parent_id=data.parent_id
            )

            repo.crear(categoria)

            session.flush()
            session.refresh(categoria)

        return categoria

    except Exception as e:

        print("ERROR REAL:")
        print(e)

        raise e


# =========================================================
# GET ALL
# =========================================================
def listar_categorias_service(
    session: Session,
    nombre: Optional[str] = None,
    offset: int = 0,
    limit: int = 10
):

    repo = CategoriaRepository(session)

    return repo.listar(
        nombre=nombre,
        offset=offset,
        limit=limit
    )


# =========================================================
# GET BY ID
# =========================================================
def obtener_categoria_service(session: Session, categoria_id: int):

    repo = CategoriaRepository(session)

    categoria = repo.obtener_por_id(categoria_id)

    if not categoria or categoria.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return categoria


# =========================================================
# UPDATE
# =========================================================
def actualizar_categoria_service(
    session: Session,
    categoria_id: int,
    data: CategoriaUpdate
):

    try:

        repo = CategoriaRepository(session)

        categoria = repo.obtener_por_id(categoria_id)

        if not categoria or categoria.deleted_at is not None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

        # VALIDAR CATEGORÍA PADRE
        if data.parent_id is not None:

            if data.parent_id == categoria_id:
                raise HTTPException(
                    status_code=400,
                    detail="Una categoría no puede ser su propia padre"
                )

            parent = repo.obtener_por_id(data.parent_id)

            if not parent or parent.deleted_at is not None:
                raise HTTPException(
                    status_code=404,
                    detail="Categoría padre no encontrada"
                )

        with UnitOfWork(session):

            if data.nombre is not None:
                categoria.nombre = data.nombre

            if data.descripcion is not None:
                categoria.descripcion = data.descripcion

            if data.imagen_url is not None:
                categoria.imagen_url = data.imagen_url

            if data.parent_id is not None:
                categoria.parent_id = data.parent_id

            categoria.updated_at = datetime.utcnow()

            session.add(categoria)
            session.flush()

        return categoria

    except Exception as e:

        print("ERROR REAL:")
        print(e)

        raise e


# =========================================================
# DELETE (SOFT DELETE)
# =========================================================
def eliminar_categoria_service(session: Session, categoria_id: int):

    try:

        categoria = session.get(Categoria, categoria_id)

        if not categoria or categoria.deleted_at is not None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada"
            )

        with UnitOfWork(session):

            session.query(ProductoCategoria).filter(
                ProductoCategoria.categoria_id == categoria_id
            ).delete()

            categoria.deleted_at = datetime.utcnow()
            categoria.updated_at = datetime.utcnow()

            session.add(categoria)

        return {
            "ok": True,
            "message": "Categoría eliminada correctamente"
        }

    except Exception as e:

        print("ERROR REAL:")
        print(e)

        raise e


# =========================================================
# RESTORE
# =========================================================
def restaurar_categoria_service(session: Session, categoria_id: int):

    try:

        categoria = session.get(Categoria, categoria_id)

        if not categoria or categoria.deleted_at is None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada o no eliminada"
            )

        with UnitOfWork(session):

            categoria.deleted_at = None
            categoria.updated_at = datetime.utcnow()

            session.add(categoria)
            session.flush()

        return categoria

    except Exception as e:

        print("ERROR REAL:")
        print(e)

        raise e