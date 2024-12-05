from fastapi import APIRouter, status

from app.db import SessionDep
from app.crud.dashboards import delete_dashboard

router = APIRouter()


@router.delete(
    "/dashboards/{dashboard_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Dashboards"],
)
def delete_dashboard_handler(dashboard_id: int, session: SessionDep) -> None:
    """
    Elimina un Dashboard si no tiene ningún Board asociado.
    """
    delete_dashboard(dashboard_id, session)
