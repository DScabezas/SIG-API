from app.models.users import User, UserCreate, UserUpdate
from app.db import SessionDep
from fastapi import APIRouter, status, HTTPException
from sqlmodel import select

router = APIRouter()


# Crear usuario
@router.post("/users", response_model=User, tags=["Users"])
async def create_user(user_data: UserCreate, session: SessionDep):
    user = User(**user_data.dict())
    session.add(user)
    session.commit()  # El objeto es automáticamente sincronizado con la base de datos
    return user


# Listar a todos los usuarios
@router.get("/users/", response_model=list[User], tags=["Users"])
async def list_users(session: SessionDep):
    return session.execute(select(User)).scalars().all()


# Buscar usuario con id específico
@router.get("/users/{id}", response_model=User, tags=["Users"])
async def get_user(id: int, session: SessionDep):
    user_db = session.get(User, id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe"
        )
    return user_db


# Eliminar usuario
@router.delete("/users/{id}", tags=["Users"])
async def delete_user(id: int, session: SessionDep):
    user_db = session.get(User, id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe"
        )
    session.delete(user_db)
    session.commit()
    return {"detail": "Usuario eliminado con éxito"}


# Actualizar usuario
@router.patch("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe"
        )

    session.add(user_db)
    session.commit()
    return user_db
