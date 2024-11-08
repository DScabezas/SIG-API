from fastapi import FastAPI
from models.roles import Roles
from models.users import UserCreate, User
from models.kpis import Kpi
from models.records import Record
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)


@app.get("/")
async def root():
    return {"message": "Hola, Dario!"}


# Crear usuario
@app.post("/users", response_model=User, tags=["Users"])
async def create_user(user_data: UserCreate, session: SessionDep):
    user = User(**user_data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Listar a todos los usuarios
@app.get("/users/", response_model=list[User], tags=["Users"])
async def list_users(session: SessionDep):
    users = session.query(User).all()
    return users


# Buscar a usuario con id especifico
@app.get("/users/{id}", response_model=User, tags=["Users"])
async def get_user(id: int, session: SessionDep):
    user = session.query(User).filter(User.id == id).first()
    return user


@app.delete("/users/{id}", response_model=User, tags=["Users"])
async def delete_user(id: int, session: SessionDep):
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()
    return user


@app.post("/kpis", tags=["Kpis"])
async def create_kpi(kpi_data: Kpi, session: SessionDep):
    session.add(kpi_data)
    session.commit()
    session.refresh(kpi_data)
    return kpi_data


@app.post("/records", tags=["Records"])
async def create_record(record_data: Record, session: SessionDep):
    session.add(record_data)
    session.commit()
    session.refresh(record_data)
    return record_data


@app.get("/roles/", response_model=list[Roles], tags=["Roles"])
async def list_users(session: SessionDep):
    roles = session.query(User).all()
    return roles
