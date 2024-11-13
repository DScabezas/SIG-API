from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models.boardusers import BoardUsers
from app.models.dboards import DBoards
from app.models.boards import Board, BoardBase
from app.models.dashboards import Dashboard
from app.models.users import User
from app.db import SessionDep

router = APIRouter()


@router.post(
    "/boards/",
    response_model=Board,
    status_code=status.HTTP_201_CREATED,
    tags=["Boards"],
)
def create_board(user_ids: list[int], board_data: BoardBase, session: SessionDep):
    """
    Crea un nuevo board y lo asocia a los usuarios y dashboards especificados.

    - **user_ids**: Lista de IDs de usuarios a asociar con el board.
    - **board_data**: Datos del board a crear.
    - **session**: Sesión de base de datos.

    Valida que los usuarios existan y que tengan un dashboard asociado.
    Si alguno de los usuarios no existe o no tiene un dashboard, se devuelve un error.
    """
    users = session.exec(select(User).where(User.id.in_(user_ids))).all()
    if len(users) != len(user_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Some users not found"
        )

    board = Board(name=board_data.name)
    session.add(board)
    session.commit()
    session.refresh(board)

    for user_id in user_ids:
        dashboard = session.exec(
            select(Dashboard).join(DBoards).where(DBoards.user_id == user_id)
        ).first()
        if not dashboard:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} has no dashboard",
            )

        session.add(
            DBoards(board_id=board.id, dashboard_id=dashboard.id, user_id=user_id)
        )

    session.commit()
    return board


@router.get(
    "/boards/{board_id}",
    response_model=Board,
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def get_board(board_id: int, session: SessionDep):
    """
    Obtiene los detalles de un board específico por su ID.

    - **board_id**: ID del board a recuperar.
    - **session**: Sesión de base de datos.

    Devuelve un error 404 si el board no se encuentra.
    """
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )
    return board


@router.put(
    "/boards/{board_id}",
    response_model=Board,
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def update_board(board_id: int, name: str, session: SessionDep):
    """
    Actualiza el nombre de un board existente.

    - **board_id**: ID del board a actualizar.
    - **name**: Nuevo nombre del board.
    - **session**: Sesión de base de datos.

    Devuelve un error 404 si el board no se encuentra.
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
def delete_board(board_id: int, session: SessionDep):
    """
    Elimina un board por su ID.

    - **board_id**: ID del board a eliminar.
    - **session**: Sesión de base de datos.

    Devuelve un error 404 si el board no se encuentra.
    """
    db_board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not db_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    session.delete(db_board)
    session.commit()
    return {"message": "Board deleted successfully"}


@router.get(
    "/dashboard/{dashboard_id}/boards",
    response_model=list[Board],
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def get_dashboard_boards(dashboard_id: int, session: SessionDep):
    """
    Obtiene todos los boards asociados a un dashboard específico.

    - **dashboard_id**: ID del dashboard del que se quieren obtener los boards.
    - **session**: Sesión de base de datos.

    Devuelve un error 404 si el dashboard no se encuentra.
    """
    dashboard = session.exec(
        select(Dashboard).where(Dashboard.id == dashboard_id)
    ).first()
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found"
        )

    boards = session.exec(
        select(Board).join(DBoards).where(DBoards.dashboard_id == dashboard_id)
    ).all()
    return boards
