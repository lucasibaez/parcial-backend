from typing import List, Annotated
from app.schemas.paginacion import PaginatedResponse
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db import get_session

# Schemas
from app.schemas.producto import (
    ProductoCreate,
    ProductoRead,
    ProductoUpdate
)

# Services
from app.services.producto import (
    listar_productos_service,
    obtener_producto_service,
    crear_producto_service,
    actualizar_producto_service,
    eliminar_producto_service,
    
    restaurar_producto_service
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# =========================
# GET ALL
# =========================
@router.get(
    "/",
    response_model=PaginatedResponse[ProductoRead],
    status_code=200
)
def listar_productos(

    
    nombre: Annotated[
        str | None,
        Query(description="Filtrar productos por nombre")
    ] = None,

    disponible: Annotated[
        bool | None,
        Query(description="Filtrar por disponibilidad")
    ] = None,

    
    offset: Annotated[
        int,
        Query(ge=0, description="Desde qué registro empezar")
    ] = 0,

    limit: Annotated[
        int,
        Query(ge=1, le=100, description="Cantidad máxima de resultados")
    ] = 10,

    session: Session = Depends(get_session)

):

    return listar_productos_service(
        session=session,
        nombre=nombre,
        disponible=disponible,
        offset=offset,
        limit=limit
    )


# =========================
# GET BY ID
# =========================
@router.get(
    "/{producto_id}",
    response_model=ProductoRead,
    status_code=200
)
def obtener_producto(

    producto_id: int,

    incluir_relaciones: Annotated[
        bool,
        Query(description="Incluir categorías e ingredientes")
    ] = True,

    session: Session = Depends(get_session)

):

    return obtener_producto_service(
        session=session,
        producto_id=producto_id,
        incluir_relaciones=incluir_relaciones
    )


# =========================
# CREATE
# =========================
@router.post(
    "/",
    response_model=ProductoRead,
    status_code=201
)
def crear_producto(

    data: ProductoCreate,

    validar_relaciones: Annotated[
        bool,
        Query(description="Validar existencia de relaciones")
    ] = True,

    session: Session = Depends(get_session)

):

    return crear_producto_service(
        session=session,
        data=data,
        validar_relaciones=validar_relaciones
    )


# =========================
# UPDATE
# =========================
@router.put("/{producto_id}", response_model=ProductoRead,status_code=200)
def actualizar_producto(

    producto_id: int,

    data: ProductoUpdate,

       session: Session = Depends(get_session)
):

    return actualizar_producto_service(
        session=session,
        producto_id=producto_id,
        data=data
    
    )


# =========================
# DELETE
# =========================
@router.delete(
    "/{producto_id}",
    status_code=200
)
def eliminar_producto(

    producto_id: int,

    session: Session = Depends(get_session)

):

    return eliminar_producto_service(
        session=session,
        producto_id=producto_id
    )


# =========================
# RESTORE
# =========================
@router.post(
    "/{producto_id}/restaurar",
    response_model=ProductoRead,
    status_code=200
)
def restaurar_producto(

    producto_id: int,

    incluir_relaciones: Annotated[
        bool,
        Query(description="Incluir relaciones")
    ] = True,

    session: Session = Depends(get_session)

):

    return restaurar_producto_service(
        session=session,
        producto_id=producto_id,
        incluir_relaciones=incluir_relaciones
    )
