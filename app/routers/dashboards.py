from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.db import SessionDep
from app.models.users import User
from app.models.dashboards import Dashboard
from app.schemas.dahboards import DashboardRead

router = APIRouter()


@router.post(
    "/dashboards/",
    response_model=Dashboard,
    status_code=status.HTTP_201_CREATED,
    tags=["Dashboards"],
)
def create_dashboard(user_id: int, session: SessionDep) -> Dashboard:
    """
    Crea un nuevo dashboard para un usuario.

    - **user_id**: ID del usuario para el cual se creará el dashboard.

    Verifica si el usuario existe y si ya tiene un dashboard. Si el usuario no existe o ya tiene un dashboard, lanza una excepción.
    Si el usuario es válido y no tiene un dashboard, se crea uno nuevo.

    Retorna el dashboard recién creado con un código de estado 201.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    if session.exec(select(Dashboard).where(Dashboard.user_id == user_id)).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a dashboard",
        )

    dashboard = Dashboard(user_id=user_id)
    session.add(dashboard)
    session.commit()
    session.refresh(dashboard)

    return dashboard


@router.get(
    "/user/{user_id}/dashboard",
    response_model=Dashboard,
    status_code=status.HTTP_200_OK,
    tags=["Dashboards"],
)
def get_user_dashboard(user_id: int, session: SessionDep) -> Dashboard:
    """
    Obtiene el Dashboard de un Usuario.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user or not user.dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User or Dashboard not found"
        )
    return user.dashboard


@router.delete(
    "/dashboards/{dashboard_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Dashboards"],
)
def delete_dashboard(dashboard_id: int, session: SessionDep) -> None:
    """
    Elimina un Dashboard si no tiene ningún Board asociado.

    - **dashboard_id**: ID del dashboard a eliminar.

    Verifica si el dashboard existe y si tiene algún board asociado. Si tiene boards, lanza una excepción.
    Si no tiene boards, elimina el dashboard y retorna un código de estado 204.
    """
    dashboard = session.exec(
        select(Dashboard).where(Dashboard.id == dashboard_id)
    ).first()
    if not dashboard:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dashboard not found")

    if dashboard.boards:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dashboard has associated boards and cannot be deleted",
        )

    session.delete(dashboard)
    session.commit()


@router.get("/dashboards/", response_model=list[DashboardRead], tags=["Dashboards"])
def list_dashboards(session: SessionDep) -> list[DashboardRead]:
    """
    Lista todos los dashboards con sus boards asociados.

    Retorna una lista con todos los dashboards y sus boards en la base de datos.
    """
    dashboards = session.exec(select(Dashboard)).all()
    return dashboards
