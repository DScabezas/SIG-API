import uuid
from fastapi import APIRouter, status
from typing import List
from app.crud.boards import (
    create_board,
    create_boards,
    get_board,
    list_boards,
    list_boards_user,
    update_board,
    delete_board,
    delete_dboard,
)
from app.db import SessionDep
from app.models.boards import Board
from app.schemas.boards import BoardCreate, BoardCreateUsers, BoardRead, BoardUpdate
from app.schemas.users import UserRead, UserReadBoards

router = APIRouter()


@router.post(
    "/boards/single-user/", status_code=status.HTTP_201_CREATED, tags=["Boards"]
)
def create_board_for_single_user(board_data: BoardCreate, session: SessionDep):
    """
    Crea un nuevo Board y lo asocia al usuario especificado.
    El user_id debe ser enviado como parte del cuerpo del JSON.
    """
    return create_board(board_data, session)


@router.post(
    "/boards/multiple-users/", status_code=status.HTTP_201_CREATED, tags=["Boards"]
)
def create_board_for_users(board_data: BoardCreateUsers, session: SessionDep):
    """
    Crea un nuevo Board y lo asocia con los usuarios especificados.
    Una lista de user_ids deben ser enviados como parte del cuerpo del JSON.
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
    Lista todos los boards en la base de datos, incluyendo los usuarios asociados.
    """
    return list_boards(session)


@router.get(
    "/boards/user/{user_id}",
    response_model=List[Board],
    status_code=status.HTTP_200_OK,
    tags=["Boards"],
)
def list_boards_handler_user(user_id: uuid.UUID, session: SessionDep):
    """
    Lista todos los boards asociados a un usuario específico mediante su ID.
    """
    return list_boards_user(user_id, session)
