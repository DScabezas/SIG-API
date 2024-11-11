from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from sqlmodel import select
from app.models.users import User, UserBase

router = APIRouter()


# Crear usuario
@router.post("/users", response_model=User, tags=["Users"])
async def create_user(user_data: UserBase, session: SessionDep):
    user = User(**user_data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Leer usuarios
@router.get("/users", response_model=list[User], tags=["Users"])
async def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users


# Leer un usuario por ID
@router.get("/users/{user_id}", response_model=User, tags=["Users"])
async def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
