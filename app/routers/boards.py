from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import List
from app.models.dboards import DBoards
from app.models.boards import Board
from app.models.dashboards import Dashboard
from app.models.users import User
from app.db import SessionDep
from app.schemas.boards import BoardCreate

router = APIRouter()


@router.post("/boards/", response_model=Board, tags=["Boards"])
def create_board(board_data: BoardCreate, session: SessionDep) -> Board:
    # Verifica que los usuarios existan
    users = session.exec(select(User).where(User.id.in_(board_data.user_ids))).all()
    if len(users) != len(board_data.user_ids):
        raise HTTPException(status_code=404, detail="One or more users not found")

    # Verifica que los usuarios tengan dashboards asociados
    dashboards = session.exec(
        select(Dashboard).where(Dashboard.user_id.in_(board_data.user_ids))
    ).all()

    if len(dashboards) != len(board_data.user_ids):
        raise HTTPException(status_code=404, detail="Some users have no dashboard")

    # Crea el nuevo Board
    board = Board(name=board_data.name)
    session.add(board)
    session.commit()
    session.refresh(board)

    # Asocia los usuarios a los dashboards y el board
    for user in users:
        dashboard = next(d for d in dashboards if d.user_id == user.id)
        session.add(
            DBoards(board_id=board.id, dashboard_id=dashboard.id, user_id=user.id)
        )

    session.commit()

    return board


@router.get(
    "/boards/{board_id}",
    response_model=Board,
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def get_board(board_id: int, session: SessionDep) -> Board:
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return board


@router.put("/boards/{board_id}", response_model=Board, tags=["Boards"])
def update_board(board_id: int, session: SessionDep):
    """
    Actualiza un board existente.

    - **board_id**: ID del board que se desea actualizar.
    - **session**: Sesión de base de datos.

    Si el board no existe, se lanza una excepción. Después de la actualización,
    se devuelve el board modificado.
    """
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    db_board.name = name
    session.commit()
    session.refresh(db_board)
    return db_board


@router.delete(
    "/boards/{board_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Boards"]
)
def delete_board(board_id: int, session: SessionDep) -> None:
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    session.delete(db_board)
    session.commit()
    return {"message": "Board deleted successfully"}


@router.get(
    "/board/{board_id}/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    tags=["Users", "Boards"],
)
def get_board_users(board_id: int, session: SessionDep) -> List[User]:
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    users = session.exec(
        select(User).join(DBoards).where(DBoards.board_id == board_id)
    ).all()
    return users
