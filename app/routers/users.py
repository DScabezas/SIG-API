from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from sqlmodel import select
from app.models.users import User, UserBase
from app.schemas.users import UserRead, UserUpdate
from app.models.boards import Board

router = APIRouter()


@router.post(
    "/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"]
)
def create_user(user: UserBase, session: SessionDep):
    """
    Crea un nuevo usuario en la base de datos.

    - **user**: Esquema de entrada que contiene los datos del usuario a crear.
    - **session**: Dependencia de sesión de base de datos.

    Retorna el usuario creado con un código de estado 201.
    """
    db_user = User(name=user.name, description=user.description, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user(user_id: int, session: SessionDep):
    """
    Obtiene un usuario por su ID.

    - **user_id**: ID del usuario a recuperar.
    - **session**: Dependencia de sesión de base de datos.

    Retorna el usuario si es encontrado. Lanza una excepción 404 si el usuario no existe.
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get(
    "/users/",
    response_model=list[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def list_users(session: SessionDep):
    """
    Lista todos los usuarios en la base de datos.

    - **session**: Dependencia de sesión de base de datos.

    Retorna una lista de todos los usuarios.
    """
    users = session.exec(select(User)).all()
    return users


@router.put(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def update_user(user_id: int, user: UserUpdate, session: SessionDep) -> User:
    """
    Actualiza un usuario existente en la base de datos.

    - **user_id**: ID del usuario a actualizar.
    - **user**: Esquema de actualización con los campos a modificar.
    - **session**: Dependencia de sesión de base de datos.

    Retorna el usuario actualizado. Lanza una excepción 404 si el usuario no existe.
    """
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, session: SessionDep):
    """
    Elimina un usuario de la base de datos.

    - **user_id**: ID del usuario a eliminar.
    - **session**: Dependencia de sesión de base de datos.

    Retorna un mensaje de confirmación si el usuario es eliminado. Lanza una excepción 404 si el usuario no existe.
    """
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}
