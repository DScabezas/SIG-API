from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models.kpis import Kpi
from app.models.records import Records, RecordBase
from app.db import SessionDep
from app.schemas.records import RecordCreate

router = APIRouter()


@router.post(
    "/kpis/{kpi_id}/records",
    response_model=Records,
    status_code=status.HTTP_201_CREATED,
    tags=["Records"],
)
def create_record(kpi_id: int, record_data: RecordCreate, session: SessionDep):
    kpi_exists = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )
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
    record = session.exec(select(Records).where(Records.id == record_id)).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    session.delete(record)
    session.commit()
    return


@router.get(
    "/kpis/{kpi_id}/records",
    response_model=list[Records],
    status_code=status.HTTP_200_OK,
    tags=["Records"],
)
def get_records_by_kpi(kpi_id: int, session: SessionDep):
    kpi_exists = session.exec(select(Kpi).where(Kpi.id == kpi_id)).first()
    if not kpi_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="KPI not found"
        )

    records = session.exec(select(Records).where(Records.kpi_id == kpi_id)).all()
    return records
