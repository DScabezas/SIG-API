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
    - **session**: Dependencia de la sesión de base de datos.

    Verifica si el usuario existe y si ya tiene un dashboard. Si el usuario no existe o ya tiene un dashboard, lanza una excepción.
    Si el usuario es válido y no tiene un dashboard, se crea uno nuevo.

    Retorna el dashboard recién creado con un código de estado 201.
    """
    user_exists = session.exec(select(User).where(User.id == user_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    existing_dashboard = session.exec(
        select(Dashboard).where(Dashboard.user_id == user_id)
    ).first()
    if existing_dashboard:
        raise HTTPException(status_code=400, detail="User already has a dashboard")

    dashboard = Dashboard(user_id=user_id)
    session.add(dashboard)
    session.commit()
    session.refresh(dashboard)

    return dashboard


@router.get("/dashboards/{user_id}", response_model=Dashboard, tags=["Dashboards"])
def get_dashboard(user_id: int, session: SessionDep) -> Dashboard:
    """
    Obtiene el dashboard de un usuario por su ID.

    - **user_id**: ID del usuario cuyo dashboard se desea obtener.
    - **session**: Dependencia de la sesión de base de datos.

    Realiza una consulta para obtener el dashboard asociado al usuario especificado.
    Si el usuario no tiene un dashboard, lanza una excepción 404.

    Retorna el dashboard encontrado o una excepción 404 si no se encuentra.
    """
    dashboard = session.exec(
        select(Dashboard)
        .join(User, Dashboard.user_id == User.id)
        .where(User.id == user_id)
    ).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found for this user")
    return dashboard


@router.get("/dashboards/", response_model=list[DashboardRead], tags=["Dashboards"])
def list_dashboards(session: SessionDep) -> list[DashboardRead]:
    """
    Lista todos los dashboards con sus boards asociados.

    - **session**: Dependencia de la sesión de base de datos.

    Retorna una lista con todos los dashboards y sus boards en la base de datos.
    """
    dashboards = session.exec(select(Dashboard)).all()
    return dashboards
