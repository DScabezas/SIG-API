from typing import List
from fastapi import APIRouter, status
from app.db import SessionDep
from app.schemas.users import UserRead, UserBase, UserUpdate
from app.crud.users import (
    create_user,
    get_user,
    list_users,
    update_user,
    delete_user,
    get_board_users,
)

router = APIRouter()


@router.post(
    "/users/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user_handler(user: UserBase, session: SessionDep):
    return create_user(user, session)


@router.get(
    "/users/{user_id}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user_handler(user_id: int, session: SessionDep):
    return get_user(user_id, session)


@router.get(
    "/users/",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def list_users_handler(session: SessionDep):
    return list_users(session)


@router.put("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def update_user_handler(user_id: int, user: UserUpdate, session: SessionDep):
    update_user(user_id, user, session)


@router.delete(
    "/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"]
)
def delete_user_handler(user_id: int, session: SessionDep):
    delete_user(user_id, session)


@router.get(
    "/board/{board_id}/users",
    response_model=List[UserRead],
    status_code=status.HTTP_200_OK,
    tags=["Users", "Boards"],
)
def get_board_users_handler(board_id: int, session: SessionDep):
    return get_board_users(board_id, session)
