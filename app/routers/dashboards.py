from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from app.models.boards import Board
from app.models.users import User
from app.models.dashboards import Dashboard

router = APIRouter()


# Crear un Dashboard solo con el ID del usuario (se crea un Board si no existe)
@router.post("/users/{user_id}/dashboard", tags=["Dashboards"])
async def create_dashboard_for_user(user_id: int, session: SessionDep):
    # Verificar si el usuario existe
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar si el usuario ya tiene un dashboard
    existing_dashboard = (
        session.query(Dashboard).filter(Dashboard.user_id == user_id).first()
    )
    if existing_dashboard:
        raise HTTPException(status_code=400, detail="User already has a dashboard")

    # Crear un Board si no existe
    board = Board(
        name=f"Board for {user.name}"
    )  # Puedes personalizar el nombre del Board
    session.add(board)
    session.commit()
    session.refresh(board)

    # Crear el Dashboard y asociarlo con el User y el Board
    dashboard = Dashboard(user_id=user_id, board_id=board.id)
    session.add(dashboard)
    session.commit()

    return dashboard


# Relacionar un usuario con un board
@router.post("/users/{user_id}/boards/{board_id}", tags=["Dashboards"])
async def add_user_to_board(user_id: int, board_id: int, session: SessionDep):
    user = session.get(User, user_id)
    board = session.get(Board, board_id)
    if not user or not board:
        raise HTTPException(status_code=404, detail="User or Board not found")

    dashboard = Dashboard(user_id=user_id, board_id=board_id)
    session.add(dashboard)
    session.commit()
    return {"message": "User added to board successfully"}


# Leer boards de un usuario
@router.get("/users/{user_id}/boards", response_model=list[Board], tags=["Dashboards"])
async def get_user_boards(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return [dashboard.board for dashboard in user.dashboards]


# Leer usuarios de un board
@router.get("/boards/{board_id}/users", response_model=list[User], tags=["Dashboards"])
async def get_board_users(board_id: int, session: SessionDep):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    return [dashboard.user for dashboard in board.dashboards]
