from fastapi import APIRouter, HTTPException
from app.db import SessionDep
from sqlmodel import select
from app.models.kpis import Kpi, KpiBase
from app.models.catalogs import Catalogo

router = APIRouter()


@router.post("/catalogos/{catalogo_id}/kpis", response_model=Kpi, tags=["KPIs"])
async def create_kpi(kpi_data: KpiBase, catalogo_id: int, session: SessionDep):
    # Recuperar el catálogo
    catalogo = session.get(Catalogo, catalogo_id)
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catalogo not found")

    # Recuperar el usuario relacionado con el catálogo
    user = session.get(User, catalogo.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Crear el KPI y asociarlo con el catálogo
    kpi = Kpi(**kpi_data.dict(), catalogo_id=catalogo_id)
    session.add(kpi)
    session.commit()
    session.refresh(kpi)

    return kpi


# Leer KPIs de un catálogo
@router.get("/catalogos/{catalogo_id}/kpis", response_model=list[Kpi], tags=["KPIs"])
async def read_kpis(catalogo_id: int, session: SessionDep):
    catalogo = session.get(Catalogo, catalogo_id)
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catalogo not found")

    return catalogo.kpis
