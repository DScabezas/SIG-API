from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from app.schemas.dahboards import DashboardRead
from app.models.dashboards import Dashboard
from app.crud.dashboards import (
    create_dashboard,
    get_user_dashboard,
    delete_dashboard,
    list_dashboards,
)

router = APIRouter()


@router.post(
    "/dashboards/",
    response_model=Dashboard,
    status_code=status.HTTP_201_CREATED,
    tags=["Dashboards"],
)
def create_dashboard_handler(user_id: int, session: SessionDep) -> Dashboard:
    """
    Crea un nuevo dashboard para un usuario.
    """
    return create_dashboard(user_id, session)


@router.get(
    "/user/{user_id}/dashboard",
    response_model=Dashboard,
    status_code=status.HTTP_200_OK,
    tags=["Dashboards"],
)
def get_user_dashboard_handler(user_id: int, session: SessionDep) -> Dashboard:
    """
    Obtiene el Dashboard de un Usuario.
    """
    return get_user_dashboard(user_id, session)


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
