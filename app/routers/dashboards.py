from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import SessionDep
from app.models.users import User
from app.models.dashboards import Dashboard

router = APIRouter()


@router.post("/dashboards/", response_model=Dashboard, tags=["Dashboards"])
def create_dashboard(user_id: int, session: SessionDep):
    # Verificamos si el usuario existe
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificamos si el usuario ya tiene un dashboard
    existing_dashboard = session.exec(
        select(Dashboard).where(Dashboard.user_id == user_id)
    ).first()
    if existing_dashboard:
        raise HTTPException(status_code=400, detail="User already has a dashboard")

    # Creamos el nuevo dashboard
    dashboard = Dashboard(user_id=user_id)
    session.add(dashboard)
    session.commit()
    session.refresh(dashboard)

    return dashboard


@router.get("/dashboards/{user_id}", response_model=Dashboard, tags=["Dashboards"])
def get_dashboard(user_id: int, session: SessionDep):
    # Buscamos el dashboard del usuario
    dashboard = session.exec(
        select(Dashboard).where(Dashboard.user_id == user_id)
    ).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found for this user")
    return dashboard
