from fastapi import APIRouter, HTTPException, status
from app.models.catalogs import CatalogoBase, Catalogo
from app.models.boards import Board
from app.db import SessionDep
from sqlalchemy import select
from typing import List

router = APIRouter()


@router.post(
    "/boards/{board_id}/catalogos",
    response_model=Catalogo,
    status_code=status.HTTP_201_CREATED,
    tags=["Catalogs"],
)
def create_catalogo(board_id: int, catalog: CatalogoBase, session: SessionDep):
    """
    Crea un nuevo catalogo para un board dado.

    - **board_id**: ID del board al que se va a asociar el catalogo.
    - **catalog**: Objeto CatalogoBase que contiene el nombre del catalogo.
    - **session**: Sesión de base de datos.

    Si el board no existe, se lanza una excepción HTTP 404.
    """
    stmt = select(Board).where(Board.id == board_id)
    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    catalogo = Catalogo(**catalog.model_dump(), board_id=board_id)
    session.add(catalogo)
    session.commit()
    session.refresh(catalogo)

    return catalogo


@router.get(
    "/catalogos",
    response_model=List[Catalogo],
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogos(session: SessionDep):
    """
    Obtiene todos los catálogos disponibles.

    - **session**: Sesión de base de datos.
    """
    stmt = select(Catalogo)
    result = session.execute(stmt).scalars().all()
    return result


@router.get(
    "/boards/{board_id}/catalogos",
    response_model=List[Catalogo],
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogos_by_board(board_id: int, session: SessionDep):
    """
    Obtiene todos los catálogos de un board dado.

    - **board_id**: ID del board del que se quieren obtener los catálogos.
    - **session**: Sesión de base de datos.

    Si el board no existe, se lanza una excepción HTTP 404.
    """
    stmt = select(Board).where(Board.id == board_id)
    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    stmt = select(Catalogo).where(Catalogo.board_id == board_id)
    result = session.execute(stmt).scalars().all()
    return result


@router.get(
    "/catalogos/{catalogo_id}",
    response_model=Catalogo,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def get_catalogo(catalogo_id: int, session: SessionDep):
    """
    Obtiene un catálogo por su ID.

    - **catalogo_id**: ID del catálogo a obtener.
    - **session**: Sesión de base de datos.

    Si el catálogo no existe, se lanza una excepción HTTP 404.
    """
    stmt = select(Catalogo).where(Catalogo.id == catalogo_id)
    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )
    return result


@router.put(
    "/catalogos/{catalogo_id}",
    response_model=Catalogo,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def update_catalogo(catalogo_id: int, catalog: CatalogoBase, session: SessionDep):
    """
    Actualiza un catálogo por su ID.

    - **catalogo_id**: ID del catálogo a actualizar.
    - **catalog**: Objeto CatalogoBase con los nuevos datos.
    - **session**: Sesión de base de datos.

    Si el catálogo no existe, se lanza una excepción HTTP 404.
    """
    stmt = select(Catalogo).where(Catalogo.id == catalogo_id)
    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    for var, value in catalog.dict(exclude_unset=True).items():
        setattr(result, var, value)

    session.add(result)
    session.commit()
    session.refresh(result)

    return result


@router.delete(
    "/catalogos/{catalogo_id}",
    response_model=Catalogo,
    status_code=status.HTTP_200_OK,
    tags=["Catalogs"],
)
def delete_catalogo(catalogo_id: int, session: SessionDep):
    """
    Elimina un catálogo por su ID.

    - **catalogo_id**: ID del catálogo a eliminar.
    - **session**: Sesión de base de datos.

    Si el catálogo no existe, se lanza una excepción HTTP 404.
    """
    stmt = select(Catalogo).where(Catalogo.id == catalogo_id)
    result = session.execute(stmt).scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    session.delete(result)
    session.commit()

    return result
