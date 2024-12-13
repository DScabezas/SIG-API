import uuid
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.users import User
from app.models.dashboards import Dashboard


def create_dashboard(user_id: uuid.UUID, session: Session) -> Dashboard:
    """
    Crea un nuevo dashboard para un usuario.
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


def get_user_dashboard(user_id: uuid.UUID, session: Session) -> Dashboard:
    """
    Obtiene el Dashboard de un Usuario.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user or not user.dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User or Dashboard not found"
        )
    return user.dashboard


def delete_dashboard(dashboard_id: int, session: Session) -> None:
    """
    Elimina un Dashboard si no tiene ningún Board asociado.
    """
    dashboard = session.exec(
        select(Dashboard).where(Dashboard.id == dashboard_id)
    ).first()
    if not dashboard:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dashboard not found")

    session.delete(dashboard)
    session.commit()


def list_dashboards(session: Session):
    """
    Lista todos los dashboards con sus boards asociados.
    """
    dashboards = session.exec(select(Dashboard)).all()
    return dashboards
