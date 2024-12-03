from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from app.db import SessionDep
from app.models.kpis import Kpi, KpiBase
from app.models.catalogs import Catalog
from app.schemas.kpis import KpiRead, MoveKpiRequest, PositionUpdate

router = APIRouter()


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


@router.patch(
    "/kpis/{kpi_id}/position",
    response_model=Kpi,
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def update_kpi_position(
    kpi_id: int, position_data: PositionUpdate, session: SessionDep
):
    """
    Actualiza la posición de un KPI.
    """
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )

    kpi.position_index = position_data.position_index
    session.add(kpi)
    session.commit()
    session.refresh(kpi)

    return kpi


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
    "/catalogs/{catalog_id}/kpis",
    response_model=List[KpiRead],
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def get_kpis_by_catalog(catalog_id: int, session: SessionDep):
    catalog = session.exec(select(Catalog).where(Catalog.id == catalog_id)).first()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Catalog not found"
        )

    return catalog.kpis


@router.patch("/kpis/{kpi_id}/move", status_code=200)
async def move_kpi_to_another_catalog(
    kpi_id: int, kpi_data: MoveKpiRequest, session: SessionDep
):
    """
    Mueve un KPI a otro catálogo.
    """
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")

    if kpi.catalog_id != kpi_data.new_catalog_id:
        kpi.catalog_id = kpi_data.new_catalog_id

    session.commit()
    session.refresh(kpi)

    return {
        "message": "KPI moved successfully",
        "kpi_id": kpi.id,
        "new_catalog_id": kpi.catalog_id,
    }
