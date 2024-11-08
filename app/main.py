from fastapi import FastAPI
from app.models.users import UserCreate, User
from app.models.kpis import Kpi
from app.models.records import Record

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hola, Dario!"}


@app.post("/users", response_model=User, tags=["Users"])
async def create_user(user_data: UserCreate):
    user = User.model_validate(user_data.model_dump())
    return user


@app.get("/users/{id}", response_model=User, tags=["Users"])
async def get_user(user_data: User):
    return user_data


@app.post("/kpis", tags=["Kpis"])
async def create_kpi(kpi_data: Kpi):
    return kpi_data


@app.post("/records", tags=["Records"])
async def create_record(record_data: Record):
    return record_data
