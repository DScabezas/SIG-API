from fastapi import APIRouter, HTTPException, status
from app.models.kpis import Kpi, KpiBase
from app.models.catalogs import Catalog
from app.db import SessionDep
from sqlmodel import select
from typing import List

router = APIRouter()


@router.post(
    "/catalogs/{catalog_id}/kpis",
    response_model=Kpi,
    status_code=status.HTTP_201_CREATED,
    tags=["KPIs"],
)
def create_catalog_kpi(catalog_id: int, kpi_data: KpiBase, session: SessionDep):
    """
    Crea un nuevo KPI y lo asocia a un catálogo existente.

    - **catalog_id**: ID del catálogo con el cual se asociará el KPI.
    - **kpi_data**: Datos del KPI que se desea crear.
    """
    catalog = session.exec(select(Catalog).where(Catalog.id == catalog_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    kpi = Kpi(**kpi_data.model_dump(), catalog_id=catalog_id)
    session.add(kpi)
    session.commit()
    session.refresh(kpi)

    return kpi


@router.get(
    "/kpis",
    response_model=List[Kpi],
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def get_all_kpis(session: SessionDep):
    """
    Obtiene todos los KPIs disponibles.
    """
    kpis = session.exec(select(Kpi)).all()
    return kpis


@router.get(
    "/catalogs/{catalog_id}/kpis",
    response_model=List[Kpi],
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def get_kpis_by_catalog(catalog_id: int, session: SessionDep):
    """
    Obtiene todos los KPIs asociados a un catálogo dado.
    """
    catalog = session.exec(select(Catalog).where(Catalog.id == catalog_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    return catalog.kpis


@router.get(
    "/kpis/{kpi_id}",
    response_model=Kpi,
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def get_kpi(kpi_id: int, session: SessionDep):
    """
    Obtiene un KPI por su ID.
    """
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )
    return kpi


@router.put(
    "/kpis/{kpi_id}",
    response_model=Kpi,
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def update_kpi(kpi_id: int, kpi_data: KpiBase, session: SessionDep):
    """
    Actualiza un KPI por su ID.
    """
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )

    for field, value in kpi_data.model_dump(exclude_unset=True).items():
        setattr(kpi, field, value)

    session.add(kpi)
    session.commit()
    session.refresh(kpi)

    return kpi


@router.delete(
    "/kpis/{kpi_id}",
    response_model=Kpi,
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def delete_kpi(kpi_id: int, session: SessionDep):
    """
    Elimina un KPI por su ID.
    """
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )

    session.delete(kpi)
    session.commit()

    return kpi
