from typing import List
from app.models.boards import Board
from app.models.dboards import DBoards
from app.models.dashboards import Dashboard
from app.models.users import User
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.schemas.boards import BoardCreate, BoardCreateUsers


def create_board(board_data: BoardCreate, session: Session):
    """
    Crea un nuevo Board y lo asocia al usuario especificado en la tabla DBoards.

    - **user_id**: ID del usuario que se asociará al board.
    - **board_data**: Datos del board, como el nombre.

    Retorna el board creado.
    """
    user = session.exec(select(User).where(User.id == board_data.user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dashboard = session.exec(
        select(Dashboard).where(Dashboard.user_id == board_data.user_id)
    ).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="User has no dashboard")

    board = Board(name=board_data.name)
    session.add(board)
    session.commit()
    session.refresh(board)

    session.add(
        DBoards(
            board_id=board.id, dashboard_id=dashboard.id, user_id=board_data.user_id
        )
    )
    session.commit()

    return board


def create_boards(board_data: BoardCreateUsers, session: Session):
    """
    Crea un único Board y lo asocia con cada uno de los usuarios especificados en la lista de user_ids.
    """
    board = Board(name=board_data.name)
    session.add(board)
    session.commit()
    session.refresh(board)

    for user_id in board_data.user_ids:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} not found"
            )

        dashboard = session.exec(
            select(Dashboard).where(Dashboard.user_id == user_id)
        ).first()
        if not dashboard:
            raise HTTPException(
                status_code=404, detail=f"User with id {user_id} has no dashboard"
            )

        session.add(
            DBoards(board_id=board.id, dashboard_id=dashboard.id, user_id=user_id)
        )

    session.commit()


def get_board(board_id: int, session: Session):
    """
    Obtiene un board por su ID.

    - **board_id**: ID del board a recuperar.

    Retorna el board encontrado o lanza una excepción si no se encuentra.
    """
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return board


def update_board(board_id: int, board_data, session: Session) -> None:
    """
    Actualiza un board existente.

    - **board_id**: ID del board a actualizar.
    - **board_data**: Datos de actualización para el board.
    """
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    db_board_data = board_data.model_dump(exclude_unset=True)
    for key, value in db_board_data.items():
        setattr(db_board, key, value)

    session.commit()
    session.refresh(db_board)


def delete_board(board_id: int, session: Session) -> None:
    """
    Elimina un board de la base de datos.

    - **board_id**: ID del board a eliminar.
    """
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    session.delete(db_board)
    session.commit()


def delete_dboard(board_id: int, session: Session):
    """
    Elimina los registros asociados en DBoards a un board.

    - **board_id**: ID del board cuyos registros en DBoards se eliminarán.
    """
    db_dboards = session.exec(select(DBoards).where(DBoards.board_id == board_id)).all()
    if not db_dboards:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No associated DBoards found"
        )

    for register in db_dboards:
        session.delete(register)

    session.commit()


def list_boards(session: Session):
    """
    Lista todos los boards en la base de datos.

    Retorna una lista de los boards con la estructura definida en el esquema BoardRead.
    """
    boards = session.exec(select(Board)).all()
    return boards
