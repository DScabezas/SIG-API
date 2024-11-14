from fastapi import APIRouter, HTTPException, status
from app.models.catalogs import CatalogBase, Catalog
from app.models.boards import Board
from app.db import SessionDep
from sqlmodel import select
from typing import List

router = APIRouter()


@router.post(
    "/boards/{board_id}/catalogos",
    response_model=Catalog,
    status_code=status.HTTP_201_CREATED,
    tags=["Catalogs"],
)
def create_catalogo(board_id: int, catalog: CatalogBase, session: SessionDep):
    """
    Crea un nuevo catálogo para un board dado.

    - **board_id**: ID del board al que se va a asociar el catálogo.
    - **catalog**: Objeto CatalogoBase con los datos del catálogo.
    """
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    catalogo = Catalog(**catalog.model_dump(), board_id=board_id)
    session.add(catalogo)
    session.commit()
    session.refresh(catalogo)
    return catalogo


@router.get(
    "/catalogos",
    response_model=List[Catalog],
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogos(session: SessionDep):
    """
    Obtiene todos los catálogos disponibles.
    """
    return session.exec(select(Catalog)).all()


@router.get(
    "/boards/{board_id}/catalogos",
    response_model=List[Catalog],
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogos_by_board(board_id: int, session: SessionDep):
    """
    Obtiene todos los catálogos de un board específico.

    - **board_id**: ID del board para filtrar los catálogos.
    """
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    return session.exec(select(Catalog).where(Catalog.board_id == board_id)).all()


@router.get(
    "/catalogos/{catalogo_id}",
    response_model=Catalog,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogo(catalogo_id: int, session: SessionDep):
    """
    Obtiene un catálogo por su ID.

    - **catalogo_id**: ID del catálogo.
    """
    catalog = session.exec(select(Catalog).where(Catalog.id == catalogo_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )
    return catalog


@router.put(
    "/catalogos/{catalogo_id}",
    response_model=Catalog,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def update_catalogo(catalogo_id: int, catalog: CatalogBase, session: SessionDep):
    """
    Actualiza un catálogo por su ID.

    - **catalogo_id**: ID del catálogo a actualizar.
    - **catalog**: Objeto CatalogoBase con los datos actualizados.
    """
    catalog_to_update = session.exec(
        select(Catalog).where(Catalog.id == catalogo_id)
    ).first()
    if not catalog_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    for var, value in catalog.model_dump(exclude_unset=True).items():
        setattr(catalog_to_update, var, value)

    session.add(catalog_to_update)
    session.commit()
    session.refresh(catalog_to_update)
    return catalog_to_update


@router.delete(
    "/catalogos/{catalogo_id}",
    response_model=Catalog,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def delete_catalogo(catalogo_id: int, session: SessionDep):
    """
    Elimina un catálogo por su ID.

    - **catalogo_id**: ID del catálogo a eliminar.
    """
    catalog_to_delete = session.exec(
        select(Catalog).where(Catalog.id == catalogo_id)
    ).first()
    if not catalog_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    session.delete(catalog_to_delete)
    session.commit()
    return catalog_to_delete
