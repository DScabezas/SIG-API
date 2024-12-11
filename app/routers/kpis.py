from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List

from app.db import SessionDep
from app.models.kpis import Kpi
from app.schemas.kpis import KpiCreate, MoveKpiRequest, PositionUpdate

router = APIRouter()


@router.get(
    "/kpis/active",
    response_model=int,
    status_code=status.HTTP_200_OK,
    tags=["KPIs"],
)
def count_all_kpis(session: SessionDep):
    """
    Obtiene todos los KPIs disponibles.
    """
    kpis = session.exec(select(Kpi)).all()
    return len(kpis)


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
def update_kpi(kpi_id: int, kpi_data: KpiCreate, session: SessionDep):
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


@router.patch("/kpis/{kpi_id}/move", status_code=200, tags=["KPIs"])
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
