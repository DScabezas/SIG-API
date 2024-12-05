from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, Session
from typing import List

from app.db import SessionDep
from app.models.kpis import Kpi
from app.models.records import Records
from app.schemas.records import RecordCreate

router = APIRouter()


def get_kpi(session: Session, kpi_id: int) -> Kpi:
    kpi = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI no encontrado"
        )
    return kpi


@router.post(
    "/kpis/{kpi_id}/records",
    response_model=Records,
    status_code=status.HTTP_201_CREATED,
    tags=["Records"],
)
def create_record(kpi_id: int, record_data: RecordCreate, session: SessionDep):
    get_kpi(session, kpi_id)
    new_record = Records(**record_data.dict(), kpi_id=kpi_id)
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record


@router.delete(
    "/records/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Records"],
)
def delete_record(record_id: int, session: SessionDep):
    record = session.get(Records, record_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado"
        )
    session.delete(record)
    session.commit()


@router.get(
    "/kpis/{kpi_id}/records",
    response_model=List[Records],
    status_code=status.HTTP_200_OK,
    tags=["Records"],
)
def get_records_by_kpi(kpi_id: int, session: SessionDep):
    get_kpi(session, kpi_id)
    records = session.exec(select(Records).where(Records.kpi_id == kpi_id)).all()
    return records
