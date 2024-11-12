from fastapi import APIRouter, HTTPException, status
from app.db import SessionDep
from sqlmodel import select
from app.models.users import User, UserBase

router = APIRouter()


@router.post("/users/", response_model=User, tags=["Users"])
def create_user(user: UserBase, session: SessionDep):
    db_user = User(name=user.name, description=user.description, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user(user_id: int, session: SessionDep):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User, tags=["Users"])
def update_user(user_id: int, user: UserBase, session: SessionDep):
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.description = user.description
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, session: SessionDep):
    db_user = session.exec(select(User).where(User.id == user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}
