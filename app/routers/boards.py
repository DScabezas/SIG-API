from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select
from app.models.boards import Board, BoardBase
from app.models.users import User
from app.models.dashboards import Dashboard
from app.db import (
    SessionDep,
)

router = APIRouter()


# Crear un nuevo board
@router.post("/boards/", response_model=Board, tags=["Boards"])
async def create_board(board_data: BoardBase, user_id: int, session: SessionDep):
    # Verificar si el usuario existe
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Crear el Board
    board = Board(**board_data.dict())
    session.add(board)
    session.commit()
    session.refresh(board)

    # Crear el Dashboard para asociar con el Board y el usuario
    dashboard = Dashboard(user_id=user_id, board_id=board.id)
    session.add(dashboard)
    session.commit()

    # Retornar el board
    return board


# Leer boards
@router.get("/boards", response_model=list[Board], tags=["Boards"])
async def read_boards(session: SessionDep):
    boards = session.exec(select(Board)).all()
    return boards


# Leer un board por ID
@router.get("/boards/{board_id}", response_model=Board, tags=["Boards"])
async def read_board(board_id: int, session: SessionDep):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board
