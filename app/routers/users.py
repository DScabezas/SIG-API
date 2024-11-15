from fastapi import APIRouter, status, HTTPException
from sqlmodel import SQLModel
from app.db import SessionDep
from app.schemas.users import UserInfoRead, UserRead
from app.crud.users import authenticate_with_microsoft, delete_user, get_user_info


router = APIRouter()


class MicrosoftAuthRequest(SQLModel):
    """
    Esquema para la solicitud de autenticación con Microsoft.
    Recibe un token de autenticación de Microsoft.
    """

    token: str


@router.post(
    "/auth/microsoft",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def create_user_handler(auth_request: MicrosoftAuthRequest):
    """
    Ruta para autenticar a un usuario usando un token de Microsoft.
    Si el usuario no existe, se crea uno nuevo.

    - **auth_request**: Datos de autenticación de Microsoft, incluyendo el token.
    - **response**: Retorna la información del usuario autenticado o creado.
    """
    user = authenticate_with_microsoft(auth_request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication failed"
        )
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Users"],
)
def delete_user_handler(user_id: str):
    """
    Ruta para eliminar un usuario de la base de datos por su ID.

    - **user_id**: ID del usuario a eliminar (debe ser un UUID válido).
    - **response**: No retorna contenido si el usuario se elimina correctamente.
    """
    try:
        delete_user(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.get(
    "/{user_id}",
    response_model=UserInfoRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user_handler(user_id: str):
    """
    Obtiene la información de un usuario a partir de su ID.

    - **user_id**: ID del usuario a consultar (debe ser un UUID válido).
    - **response**: Retorna un objeto con la información del usuario.
    """
    try:
        return get_user_info(user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
