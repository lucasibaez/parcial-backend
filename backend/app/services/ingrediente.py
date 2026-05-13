from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.core.unit_of_work import UnitOfWork

from app.models.ingrediente import Ingrediente
from app.models.producto_ingrediente import ProductoIngrediente

from app.repositorios.ingrediente_repository import IngredienteRepository

from app.schemas.ingrediente import (
    IngredienteCreate,
    IngredienteUpdate
)


# =========================================================
# CREATE
# =========================================================
def crear_ingrediente_service(
    session: Session,
    data: IngredienteCreate
):

    try:

        repo = IngredienteRepository(session)

        with UnitOfWork(session):

            ingrediente = Ingrediente(
                nombre=data.nombre,
                descripcion=data.descripcion,
                es_alergeno=data.es_alergeno
            )

            repo.crear(ingrediente)

            session.flush()
            session.refresh(ingrediente)

        return ingrediente

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500,
            detail="Error interno al crear ingrediente"
        )


# =========================================================
# GET ALL
# =========================================================
def listar_ingredientes_service(
    session: Session,
    nombre: Optional[str] = None,
    es_alergeno: Optional[bool] = None,
    offset: int = 0,
    limit: int = 10
):

    repo = IngredienteRepository(session)

    return repo.listar(
        nombre=nombre,
        es_alergeno=es_alergeno,
        offset=offset,
        limit=limit
    )


# =========================================================
# GET BY ID
# =========================================================
def obtener_ingrediente_service(
    session: Session,
    ingrediente_id: int
):

    repo = IngredienteRepository(session)

    ingrediente = repo.obtener_por_id(ingrediente_id)

    if not ingrediente or ingrediente.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    return ingrediente


# =========================================================
# UPDATE
# =========================================================
def actualizar_ingrediente_service(
    session: Session,
    ingrediente_id: int,
    data: IngredienteUpdate
):

    try:

        repo = IngredienteRepository(session)

        ingrediente = repo.obtener_por_id(ingrediente_id)

        if not ingrediente or ingrediente.deleted_at is not None:
            raise HTTPException(
                status_code=404,
                detail="Ingrediente no encontrado"
            )

        with UnitOfWork(session):

            if data.nombre is not None:
                ingrediente.nombre = data.nombre

            if data.descripcion is not None:
                ingrediente.descripcion = data.descripcion

            if data.es_alergeno is not None:
                ingrediente.es_alergeno = data.es_alergeno

            ingrediente.updated_at = datetime.utcnow()

            session.add(ingrediente)
            session.flush()

        return ingrediente

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar ingrediente"
        )


# =========================================================
# DELETE (SOFT DELETE)
# =========================================================
def eliminar_ingrediente_service(
    session: Session,
    ingrediente_id: int
):

    try:

        ingrediente = session.get(Ingrediente, ingrediente_id)

        if not ingrediente or ingrediente.deleted_at is not None:
            raise HTTPException(
                status_code=404,
                detail="Ingrediente no encontrado"
            )

        with UnitOfWork(session):

            session.query(ProductoIngrediente).filter(
                ProductoIngrediente.ingrediente_id == ingrediente_id
            ).delete()

            ingrediente.deleted_at = datetime.utcnow()
            ingrediente.updated_at = datetime.utcnow()

            session.add(ingrediente)

        return {
            "ok": True,
            "message": "Ingrediente eliminado correctamente"
        }

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500,
            detail="Error interno al eliminar ingrediente"
        )


# =========================================================
# RESTORE
# =========================================================
def restaurar_ingrediente_service(
    session: Session,
    ingrediente_id: int
):

    try:

        ingrediente = session.get(Ingrediente, ingrediente_id)

        if not ingrediente or ingrediente.deleted_at is None:
            raise HTTPException(
                status_code=404,
                detail="Ingrediente no encontrado o no eliminado"
            )

        with UnitOfWork(session):

            ingrediente.deleted_at = None
            ingrediente.updated_at = datetime.utcnow()

            session.add(ingrediente)
            session.flush()

        return ingrediente

    except Exception as e:

        if isinstance(e, HTTPException):
            raise e

        raise HTTPException(
            status_code=500,
            detail="Error interno al restaurar ingrediente"
        )