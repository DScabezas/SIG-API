from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.db import SessionDep
from app.models.users import User
from app.models.dashboards import Dashboard

router = APIRouter()


@router.post(
    "/dashboards/",
    response_model=Dashboard,
    status_code=status.HTTP_201_CREATED,
    tags=["Dashboards"],
)
def create_dashboard(user_id: int, session: SessionDep) -> Dashboard:
    # Verificar si el usuario existe y si ya tiene un dashboard en una sola consulta
    user_exists = session.exec(select(User).where(User.id == user_id)).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    existing_dashboard = session.exec(
        select(Dashboard).where(Dashboard.user_id == user_id)
    ).first()
    if existing_dashboard:
        raise HTTPException(status_code=400, detail="User already has a dashboard")

    # Crear el nuevo dashboard
    dashboard = Dashboard(user_id=user_id)
    session.add(dashboard)
    session.commit()
    session.refresh(dashboard)

    return dashboard


@router.get("/dashboards/{user_id}", response_model=Dashboard, tags=["Dashboards"])
def get_dashboard(user_id: int, session: SessionDep) -> Dashboard:
    # Verificar si el usuario existe y obtener su dashboard en una única consulta
    dashboard = session.exec(
        select(Dashboard)
        .join(User, Dashboard.user_id == User.id)
        .where(User.id == user_id)
    ).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found for this user")
    return dashboard
