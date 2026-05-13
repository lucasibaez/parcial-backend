from typing import List, Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db import get_session

# Schemas
from app.schemas.categoria import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate,
    CategoriaTree
)

# Services
from app.services.categoria import (
    crear_categoria_service,
    listar_categorias_service,
    obtener_categoria_service,
    actualizar_categoria_service,
    eliminar_categoria_service,
    restaurar_categoria_service
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

# =========================================================
# CREATE
# =========================================================
@router.post(
    "/",
    response_model=CategoriaRead,
    status_code=201
)
def crear_categoria(

    data: CategoriaCreate,

    session: Session = Depends(get_session)

):

    return crear_categoria_service(
        session=session,
        data=data
    )


# =========================================================
# GET ALL
# =========================================================
@router.get(
    "/",
    response_model=List[CategoriaRead],
    status_code=200
)
def listar_categorias(

    nombre: Annotated[
        str | None,
        Query(description="Filtrar categorías por nombre")
    ] = None,

    # PAGINACIÓN
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Desde qué registro comenzar"
        )
    ] = 0,

    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Cantidad máxima de resultados"
        )
    ] = 10,

    session: Session = Depends(get_session)

):

    return listar_categorias_service(
        session=session,
        nombre=nombre,
        offset=offset,
        limit=limit
    )


# =========================================================
# GET BY ID
# =========================================================
@router.get(
    "/{id}",
    response_model=CategoriaTree,
    status_code=200
)
def obtener_categoria(

    id: int,

    session: Session = Depends(get_session)

):

    return obtener_categoria_service(
        session=session,
        categoria_id=id
    )


# =========================================================
# UPDATE
# =========================================================
@router.put(
    "/{id}",
    response_model=CategoriaRead,
    status_code=200
)
def actualizar_categoria(

    id: int,

    data: CategoriaUpdate,

    session: Session = Depends(get_session)

):

    return actualizar_categoria_service(
        session=session,
        categoria_id=id,
        data=data
    )


# =========================================================
# DELETE
# =========================================================
@router.delete(
    "/{id}",
    status_code=200
)
def eliminar_categoria(

    id: int,

    session: Session = Depends(get_session)

):

    return eliminar_categoria_service(
        session=session,
        categoria_id=id
    )


# =========================================================
# RESTORE
# =========================================================
@router.post(
    "/{id}/restaurar",
    response_model=CategoriaRead,
    status_code=200
)
def restaurar_categoria(

    id: int,

    session: Session = Depends(get_session)

):

    return restaurar_categoria_service(
        session=session,
        categoria_id=id
    )