from typing import List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.models.dboards import DBoards
from app.models.users import User
from app.models.boards import Board
from app.schemas.users import UserBase, UserUpdate


def create_user(user_data: UserBase, session: Session) -> User:
    db_user = User(
        name=user_data.name, description=user_data.description, email=user_data.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(user_id: int, session: Session) -> User:
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


def list_users(session: Session):
    return session.exec(select(User)).all()


def update_user(user_id: int, user_data: UserUpdate, session: Session) -> None:
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)


def delete_user(user_id: int, session: Session) -> None:
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(db_user)
    session.commit()


def get_board_users(board_id: int, session: Session):
    board = session.exec(select(Board).where(Board.id == board_id)).first()
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board not found"
        )

    return session.exec(
        select(User).join(DBoards).where(DBoards.board_id == board_id)
    ).all()
