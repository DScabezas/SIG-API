from fastapi import FastAPI
from app.db import SessionDep, create_all_tables
from .routers import users, records


app = FastAPI(lifespan=create_all_tables)
app.include_router(users.router)
app.include_router(records.router)


@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}
