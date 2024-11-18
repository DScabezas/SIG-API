from sqlmodel import Session, select
from app.models.users import User
from app.schemas.users import UserCreate, UserInfoRead
from pydantic import BaseModel
from uuid import UUID
import requests
from fastapi import HTTPException, status


class DeleteUserRequest(BaseModel):
    user_id: str


class GetUserInfoRequest(BaseModel):
    user_id: str


def create_user(user_data: UserCreate, session: Session) -> User:
    """
    Crea un nuevo usuario en la base de datos.

    - **user_data**: Datos del usuario a crear.

    Retorna el usuario recién creado.
    """
    db_user = User(**user_data.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def authenticate_with_microsoft(token: str, session: Session) -> User:
    microsoft_url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(microsoft_url, headers=headers)
        response.raise_for_status()
        user_info = response.json()

        user_data = {
            "id": UUID(user_info["id"]),
            "name": user_info.get("displayName"),
            "email": user_info.get("mail"),
            "given_name": user_info.get("givenName"),
            "surname": user_info.get("surname"),
            "job_title": user_info.get("jobTitle"),
            "business_phone": user_info.get("businessPhones", [None])[0],
            "mobile_phone": user_info.get("mobilePhone"),
            "office_location": user_info.get("officeLocation"),
        }

        user = session.exec(select(User).where(User.id == user_data["id"])).first()

        if not user:
            user = create_user(UserCreate(**user_data), session)

        return user
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Authentication failed"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


from uuid import UUID


def delete_user(user_id: str, session: Session) -> None:
    """
    Elimina un usuario de la base de datos.

    - **request**: Esquema con el ID del usuario a eliminar.

    Si el usuario no se encuentra, lanza una excepción HTTP 404.
    """
    user_id = request.user_id
    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format"
        )

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(user)
    session.commit()


def get_user_info(request: GetUserInfoRequest, session: Session) -> UserInfoRead:
    """
    Obtiene la información de un usuario a partir de su ID.

    - **request**: Esquema con el ID del usuario a consultar.

    Retorna un objeto con la información del usuario en formato `UserInfoRead`.
    """
    user_id = request.user_id
    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid UUID format"
        )

    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user.model_dump()
    return UserInfoRead(**user_data)
