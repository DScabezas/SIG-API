from app.models.records import Record
from app.db import SessionDep
from fastapi import APIRouter

router = APIRouter()


@router.post("/records", tags=["Records"])
async def create_record(record_data: Record, session: SessionDep):
    session.add(record_data)
    session.commit()
    session.refresh(record_data)
    return record_data
