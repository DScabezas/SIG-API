from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db import SessionDep
from app.models.boards import Board
from app.models.catalogs import Catalog, CatalogBase
from app.models.kpis import Kpi
from app.schemas.kpis import KpiCreate, KpiRead

router = APIRouter(prefix="/catalogs", tags=["Catalogs"])


@router.get("/", response_model=List[Catalog], status_code=status.HTTP_200_OK)
def get_catalogs(session: SessionDep):
    """
    Obtiene todos los catálogos disponibles.
    """
    catalogs = session.exec(select(Catalog)).all()
    return catalogs


@router.get(
    "/boards/{board_id}/", response_model=List[Catalog], status_code=status.HTTP_200_OK
)
def get_catalogs_by_board(board_id: int, session: SessionDep):
    """
    Obtiene todos los catálogos de un board específico.

    - **board_id**: ID del board para filtrar los catálogos.
    """
    board_exists = session.exec(select(Board.id).where(Board.id == board_id)).first()
    if not board_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    catalogs = session.exec(select(Catalog).where(Catalog.board_id == board_id)).all()
    return catalogs


@router.get("/{catalog_id}", response_model=Catalog, status_code=status.HTTP_200_OK)
def get_catalog(catalog_id: int, session: SessionDep):
    """
    Obtiene un catálogo por su ID.

    - **catalog_id**: ID del catálogo.
    """
    catalog = session.exec(select(Catalog).where(Catalog.id == catalog_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )
    return catalog


@router.patch("/{catalog_id}", response_model=Catalog, status_code=status.HTTP_200_OK)
def update_catalog(catalog_id: int, catalog: CatalogBase, session: SessionDep):
    """
    Actualiza un catálogo por su ID.

    - **catalog_id**: ID del catálogo a actualizar.
    - **catalog**: Objeto CatalogBase con los datos actualizados.
    """
    catalog_to_update = session.exec(
        select(Catalog).where(Catalog.id == catalog_id)
    ).first()
    if not catalog_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    update_data = catalog.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(catalog_to_update, key, value)

    session.add(catalog_to_update)
    session.commit()
    session.refresh(catalog_to_update)
    return catalog_to_update


@router.delete("/{catalog_id}", response_model=Catalog, status_code=status.HTTP_200_OK)
def delete_catalog(catalog_id: int, session: SessionDep):
    """
    Elimina un catálogo por su ID.

    - **catalog_id**: ID del catálogo a eliminar.
    """
    catalog_to_delete = session.exec(
        select(Catalog).where(Catalog.id == catalog_id)
    ).first()
    if not catalog_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    session.delete(catalog_to_delete)
    session.commit()
    return catalog_to_delete


@router.post(
    "/{catalog_id}/kpis",
    response_model=Kpi,
    status_code=status.HTTP_201_CREATED,
    tags=["KPIs"],
)
def create_catalog_kpi(catalog_id: int, kpi_data: KpiCreate, session: SessionDep):
    """
    Crea un nuevo KPI y lo asocia a un catálogo existente.

    - **catalog_id**: ID del catálogo al que se asociará el KPI.
    - **kpi_data**: Objeto KpiBase con los datos del KPI.
    """
    catalog_exists = session.exec(
        select(Catalog.id).where(Catalog.id == catalog_id)
    ).first()
    if not catalog_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    kpi = Kpi(**kpi_data.model_dump(), catalog_id=catalog_id)
    session.add(kpi)
    session.commit()
    session.refresh(kpi)
    return kpi


@router.get(
    "/{catalog_id}/kpis",
    response_model=List[KpiRead],
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def get_kpis_by_catalog(catalog_id: int, session: SessionDep):
    """
    Obtiene todos los KPIs asociados a un catálogo específico.

    - **catalog_id**: ID del catálogo para filtrar los KPIs.
    """
    catalog = session.exec(select(Catalog).where(Catalog.id == catalog_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    return catalog.kpis
