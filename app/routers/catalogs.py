from fastapi import APIRouter, HTTPException, status
from app.models.catalogs import Catalogo
from app.models.boards import Board
from app.db import SessionDep

router = APIRouter()


@router.post(
    "/boards/{board_id}/catalogos",
    response_model=Catalogo,
    status_code=status.HTTP_201_CREATED,
    tags=["Catalogs"],
)
def create_catalogo(board_id: int, session: SessionDep):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    catalogo = Catalogo(board_id=board_id)
    session.add(catalogo)
    session.commit()
    session.refresh(catalogo)

    return catalogo
