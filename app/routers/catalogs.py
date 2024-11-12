from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.db import SessionDep
from app.models.catalogs import Catalogo
from app.models.users import User

router = APIRouter()


@router.post("/catalogos/", response_model=Catalogo, tags=["Catalogs"])
def create_catalogo(user_id: int, session: SessionDep):
    # Verificamos si el usuario existe
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    catalogo = Catalogo(user_id=user_id)
    session.add(catalogo)
    session.commit()
    session.refresh(catalogo)

    return catalogo


@router.get("/catalogos/{catalogo_id}", response_model=Catalogo, tags=["Catalogs"])
def get_catalogo(catalogo_id: int, session: SessionDep):
    catalogo = session.exec(select(Catalogo).where(Catalogo.id == catalogo_id)).first()
    if not catalogo:
        raise HTTPException(status_code=404, detail="Catalogo not found")
    return catalogo


@router.put("/catalogos/{catalogo_id}", response_model=Catalogo, tags=["Catalogs"])
def update_catalogo(catalogo_id: int, session: SessionDep):
    db_catalogo = session.exec(
        select(Catalogo).where(Catalogo.id == catalogo_id)
    ).first()
    if not db_catalogo:
        raise HTTPException(status_code=404, detail="Catalogo not found")

    session.commit()
    session.refresh(db_catalogo)
    return db_catalogo


@router.delete("/catalogos/{catalogo_id}", tags=["Catalogs"])
def delete_catalogo(catalogo_id: int, session: SessionDep):
    db_catalogo = session.exec(
        select(Catalogo).where(Catalogo.id == catalogo_id)
    ).first()
    if not db_catalogo:
        raise HTTPException(status_code=404, detail="Catalogo not found")

    session.delete(db_catalogo)
    session.commit()
    return {"message": "Catalogo deleted successfully"}
