from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.models.dboards import DBoards
from app.models.boards import Board, BoardBase
from app.models.dashboards import Dashboard
from app.models.users import User
from app.db import SessionDep

router = APIRouter()


@router.post("/boards/", response_model=Board, tags=["Boards"])
def create_board(user_id: int, dashboard_id: int, name: str, session: SessionDep):
    """
    Crea un nuevo board y lo asocia a un usuario y su dashboard correspondiente.

    - **user_id**: ID del usuario que va a ser asociado con el board.
    - **dashboard_id**: ID del dashboard que va a ser asociado con el board.
    - **name**: Nombre del board a crear.
    - **session**: Sesión de base de datos.

    Valida que el usuario exista y que el dashboard pertenece al usuario.
    Si el usuario o dashboard no se encuentran, se lanza una excepción.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dashboard = session.exec(
        select(Dashboard).where(
            Dashboard.id == dashboard_id, Dashboard.user_id == user_id
        )
    ).first()
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Some users not found"
        )

    dashboards = session.exec(
        select(Dashboard).where(Dashboard.user_id.in_(user_ids))
    ).all()

    dashboards_dict = {dashboard.user_id: dashboard for dashboard in dashboards}

    for user_id in user_ids:
        if user_id not in dashboards_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} has no dashboard",
            )

    board = Board(name=board_data.name)

    session.add(board)
    session.commit()
    session.refresh(board)

    for user_id in user_ids:
        dashboard = dashboards_dict[user_id]

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
    Obtiene la información de un board específico.

    - **board_id**: ID del board que se desea obtener.
    - **session**: Sesión de base de datos.

    Si el board no existe, se lanza una excepción.
    """
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
def delete_board(board_id: int, session: SessionDep):
    """
    Elimina un board existente.

    - **board_id**: ID del board que se desea eliminar.
    - **session**: Sesión de base de datos.

    Si el board no existe, se lanza una excepción. Una vez eliminado, se
    devuelve un mensaje de éxito.
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
