from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from sqlmodel import select
from app.models.catalogs import Catalogo, CatalogoBase
from app.models.boards import Board

router = APIRouter()


# Crear un catálogo en un board específico
@router.post(
    "/boards/{board_id}/catalogos", response_model=Catalogo, tags=["Catalogos"]
)
async def create_catalogo(
    catalogo_data: CatalogoBase, board_id: int, session: SessionDep
):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    user = board.user  # Acceder al usuario asociado con el board
    if not user:
        raise HTTPException(status_code=404, detail="User not found for the board")

    # Crear el catálogo con el user_id correctamente asignado
    catalogo = Catalogo(**catalogo_data.dict(), board_id=board_id, user_id=user.id)
    session.add(catalogo)
    session.commit()
    session.refresh(catalogo)
    return catalogo


# Leer catálogos de un board
@router.get(
    "/boards/{board_id}/catalogos", response_model=list[Catalogo], tags=["Catalogos"]
)
async def read_catalogos(board_id: int, session: SessionDep):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    return board.catalogos
