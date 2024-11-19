from fastapi import APIRouter, status, HTTPException
from sqlmodel import SQLModel
from app.db import SessionDep
from app.schemas.users import UserInfoRead, UserRead
from app.crud.users import (
    authenticate_with_microsoft,
    delete_user,
    get_user_info,
    DeleteUserRequest,
    GetUserInfoRequest,
)

router = APIRouter()


class MicrosoftAuthRequest(SQLModel):
    """
    Esquema para la solicitud de autenticación con Microsoft.
    Recibe un token de autenticación de Microsoft.
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
    Ruta para autenticar a un usuario usando un token de Microsoft.
    Si el usuario no existe, se crea uno nuevo.

    - **auth_request**: Datos de autenticación de Microsoft, incluyendo el token.
    - **response**: Retorna la información del usuario autenticado o creado.
    """
    user = authenticate_with_microsoft(auth_request.token, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication failed"
        )
    return user


@router.post(
    "/users/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
)
def delete_user_handler(delete_request: DeleteUserRequest, session: SessionDep):
    """
    Ruta para eliminar un usuario de la base de datos por su ID.

    - **delete_request**: JSON con el ID del usuario a eliminar.
    """
    try:
        delete_user(delete_request.user_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.post(
    "/users/info",
    response_model=UserInfoRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user_handler(request: GetUserInfoRequest, session: SessionDep):
    """
    Obtiene la información de un usuario a partir de su ID.

    - **request**: JSON con el ID del usuario a consultar (enviado desde el frontend).
    - **response**: Retorna un objeto con la información del usuario.
    """
    try:
        return get_user_info(request, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
