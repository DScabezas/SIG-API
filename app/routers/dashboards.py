import uuid
from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from app.schemas.dahboards import DashboardCreate, DashboardRead
from app.models.dashboards import Dashboard
from app.crud.dashboards import (
    create_dashboard,
    get_user_dashboard,
    delete_dashboard,
    list_dashboards,
)

router = APIRouter()


@router.post(
    "/dashboards/user/{user_id}",
    response_model=DashboardRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Dashboards"],
)
def create_dashboard_handler(
    payload: DashboardCreate, session: SessionDep
) -> Dashboard:
    """
    Crea un nuevo dashboard para un usuario basado en un JSON con el user_id.
    """
    return create_dashboard(payload.user_id, session)


@router.get(
    "/dashboards/user/{user_id}",
    response_model=DashboardRead,
    status_code=status.HTTP_200_OK,
    tags=["Dashboards"],
)
def get_dashboard_by_user_handler(user_id: str, session: SessionDep) -> Dashboard:
    """
    Obtiene el Dashboard de un Usuario basado en un parámetro de ruta.
    """
    try:
        return get_user_dashboard(uuid.UUID(user_id), session)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format. Must be a valid UUID.",
        )


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


@router.get(
    "/dashboards/",
    response_model=list[DashboardRead],
    tags=["Dashboards"],
)
def list_dashboards_handler(session: SessionDep):
    """
    Lista todos los dashboards con sus boards asociados.
    """
    return list_dashboards(session)
