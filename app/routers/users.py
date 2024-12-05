from typing import List
import uuid

from fastapi import APIRouter, status, HTTPException
from sqlmodel import SQLModel

from app.crud.boards import list_boards_user
from app.crud.users import (
    authenticate_with_microsoft,
    count_users,
    delete_user,
    get_all_users,
    get_user_info,
    DeleteUserRequest,
    GetUserInfoRequest,
)
from app.db import SessionDep
from app.models.users import UserBase
from app.schemas.boards import BoardRead
from app.schemas.users import UserInfoRead

router = APIRouter()


class MicrosoftAuthRequest(SQLModel):
    """
    Esquema para la solicitud de autenticación con Microsoft.

    - **token**: Token de autenticación de Microsoft.
    """

    token: str


@router.post(
    "/auth/microsoft",
    response_model=UserInfoRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def create_user_handler(auth_request: MicrosoftAuthRequest, session: SessionDep):
    """
    Autentica a un usuario usando un token de Microsoft.
    Si el usuario no existe, crea uno nuevo.

    - **auth_request**: Datos de autenticación de Microsoft, incluyendo el token.
    - **response**: Información del usuario autenticado o creado.
    """
    try:
        user = authenticate_with_microsoft(auth_request.token, session=session)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}",
        )


@router.post(
    "/users/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
)
def delete_user_handler(delete_request: DeleteUserRequest, session: SessionDep) -> None:
    """
    Elimina un usuario de la base de datos por su ID.

    - **delete_request**: JSON con el ID del usuario a eliminar.
    """
    try:
        delete_user(delete_request.user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el usuario: {str(e)}",
        )


@router.post(
    "/users/info",
    response_model=UserInfoRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user_handler(request: GetUserInfoRequest, session: SessionDep) -> UserInfoRead:
    """
    Obtiene la información de un usuario a partir de su ID.

    - **request**: JSON con el ID del usuario a consultar.
    - **response**: Información del usuario.
    """
    try:
        return get_user_info(request, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la información del usuario: {str(e)}",
        )


@router.get(
    "/users",
    response_model=List[UserBase],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_all_users_handler(session: SessionDep):
    """
    Obtiene todos los usuarios registrados en la base de datos.

    - **response**: Lista de todos los usuarios.
    """
    users = get_all_users(session=session)
    return users


@router.get(
    "/users/active",
    response_model=int,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_active_users_count(session: SessionDep) -> int:
    """
    Obtiene el número de usuarios activos registrados en la base de datos.

    - **response**: Número de usuarios activos.
    """
    return count_users(session)


@router.get(
    "/users/{user_id}/boards",
    response_model=List[BoardRead],
    status_code=status.HTTP_200_OK,
    summary="Listar tableros por usuario",
    description="Recupera todos los tableros asociados a un usuario específico.",
    tags=["Boards"],
)
def list_boards_handler_user(user_id: uuid.UUID, session: SessionDep):
    """
    Recupera todos los tableros asociados a un usuario específico.

    - **user_id**: ID del usuario.
    - **response**: Lista de tableros asociados.
    """
    boards = list_boards_user(user_id, session)
    return boards
