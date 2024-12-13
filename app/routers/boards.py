from typing import List

from fastapi import APIRouter, HTTPException, status

from app.crud.boards import (
    count_board,
    create_board,
    create_boards,
    get_board,
    list_boards,
    update_board,
    delete_board,
    delete_dboard,
)
from app.db import SessionDep
from app.models.boards import Board
from app.models.catalogs import Catalog, CatalogBase
from app.schemas.boards import (
    BoardCreate,
    BoardCreateUsers,
    BoardRead,
    BoardUpdate,
)

router = APIRouter(tags=["Boards"], prefix="/boards")


@router.post(
    "/single-user/",
    response_model=BoardRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a board for a single user",
    description="Creates a new board and associates it with the specified user.",
)
def create_board_for_single_user(board_data: BoardCreate, session: SessionDep) -> Board:
    return create_board(board_data, session)


@router.post(
    "/multiple-users/",
    response_model=List[BoardRead],
    status_code=status.HTTP_201_CREATED,
    summary="Create a board for multiple users",
    description="Creates a new board and associates it with the specified list of users.",
)
def create_board_for_users(board_data: BoardCreateUsers, session: SessionDep):
    """
    Crea un nuevo Board y lo asocia con los usuarios especificados.
    Una lista de user_ids deben ser enviados como parte del cuerpo del JSON.
    """
    return create_boards(board_data, session)


@router.get(
    "/{board_id}",
    response_model=BoardRead,
    status_code=status.HTTP_200_OK,
    summary="Get a board by ID",
    description="Retrieves a board by its ID.",
)
def get_board_handler(board_id: int, session: SessionDep) -> Board:
    return get_board(board_id, session)


@router.put(
    "/{board_id}",
    response_model=BoardRead,
    status_code=status.HTTP_200_OK,
    summary="Update a board",
    description="Updates an existing board with the provided data.",
)
def update_board_handler(
    board_id: int, board: BoardUpdate, session: SessionDep
) -> Board:
    update_board(board_id, board, session)
    return get_board(board_id, session)


@router.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a board",
    description="Deletes a board and its associated records in DBoards.",
)
def delete_board_handler(board_id: int, session: SessionDep) -> None:
    delete_dboard(board_id, session)
    delete_board(board_id, session)


@router.get(
    "/",
    response_model=List[BoardRead],
    status_code=status.HTTP_200_OK,
    summary="List all boards",
    description="Retrieves a list of all boards in the database.",
)
def list_boards_handler(session: SessionDep):
    """
    Lista todos los boards en la base de datos, incluyendo los usuarios asociados.
    """
    return list_boards(session)


@router.get(
    "/count/",
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary="Count boards",
    description="Returns the total number of boards in the database.",
)
def count_boards(session: SessionDep) -> int:
    return count_board(session)


@router.post(
    "/{board_id}/catalogs/",
    response_model=Catalog,
    status_code=status.HTTP_201_CREATED,
    summary="Create a catalog for a board",
    description="Creates a new catalog and associates it with the specified board.",
)
def create_catalog(
    board_id: int,
    catalog: CatalogBase,
    session: SessionDep,
) -> Catalog:
    board = get_board(board_id, session)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    new_catalog = Catalog(**catalog.model_dump(), board_id=board_id)
    session.add(new_catalog)
    session.commit()
    session.refresh(new_catalog)
    return new_catalog
