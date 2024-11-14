from fastapi import APIRouter, status
from typing import List
from app.crud.boards import (
    create_board,
    create_boards,
    get_board,
    list_boards,
    update_board,
    delete_board,
    delete_dboard,
)
from app.db import SessionDep
from app.schemas.boards import BoardCreate, BoardCreateUsers, BoardRead, BoardUpdate

router = APIRouter()


@router.post("/boards/{user_id}/", status_code=status.HTTP_201_CREATED, tags=["Boards"])
def create_board_for_single_user(
    user_id: int, board_data: BoardCreate, session: SessionDep
):
    """
    Crea un nuevo Board y lo asocia al usuario especificado.
    """
    return create_board(user_id, board_data, session)


@router.post("/boards/", status_code=status.HTTP_201_CREATED, tags=["Boards"])
def create_board_for_users(board_data: BoardCreateUsers, session: SessionDep):
    """
    Crea un nuevo Board y lo asocia con cada uno de los usuarios especificados en la lista de user_ids.
    """
    return create_boards(board_data, session)


@router.get("/boards/{board_id}", response_model=BoardRead, tags=["Boards"])
def get_board_handler(board_id: int, session: SessionDep):
    """
    Obtiene un board por su ID.
    """
    return get_board(board_id, session)


@router.put(
    "/boards/{board_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Boards"]
)
def update_board_handler(
    board_id: int, board: BoardUpdate, session: SessionDep
) -> None:
    """
    Actualiza un board existente.
    """
    update_board(board_id, board, session)


@router.delete(
    "/boards/{board_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Boards"]
)
def delete_board_handler(board_id: int, session: SessionDep) -> None:
    """
    Elimina un board de la base de datos, incluyendo los registros asociados en DBoards.
    """
    delete_dboard(board_id, session)
    delete_board(board_id, session)


@router.get(
    "/boards/",
    response_model=List[BoardRead],
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def list_boards_handler(session: SessionDep):
    """
    Lista todos los boards en la base de datos.
    """
    return list_boards(session)
