from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.dboards import DBoards
from app.models.boards import Board
from app.models.dashboards import Dashboard
from app.models.users import User
from app.db import SessionDep
from fastapi import APIRouter

router = APIRouter()


@router.post("/boards/", response_model=Board, tags=["Boards"])
def create_board(user_id: int, dashboard_id: int, name: str, session: SessionDep):
    # Verificar si el usuario existe
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar si el dashboard existe y pertenece al usuario
    dashboard = session.exec(
        select(Dashboard).where(
            Dashboard.id == dashboard_id, Dashboard.user_id == user_id
        )
    ).first()
    if not dashboard:
        raise HTTPException(
            status_code=404, detail="Dashboard not found or does not belong to user"
        )

    # Crear el board con el nombre especificado
    board = Board(name=name)
    session.add(board)
    session.commit()
    session.refresh(board)

    # Crear la relación en la tabla intermedia DBoards
    dboard_relation = DBoards(dashboard_id=dashboard_id, board_id=board.id)
    session.add(dboard_relation)
    session.commit()

    return board


@router.get("/boards/{board_id}", response_model=Board, tags=["Boards"])
def get_board(board_id: int, session: SessionDep):
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.put("/boards/{board_id}", response_model=Board, tags=["Boards"])
def update_board(board_id: int, session: SessionDep):
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")

    session.commit()
    session.refresh(db_board)
    return db_board


@router.delete("/boards/{board_id}", tags=["Boards"])
def delete_board(board_id: int, session: SessionDep):
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")

    session.delete(db_board)
    session.commit()
    return {"message": "Board deleted successfully"}
