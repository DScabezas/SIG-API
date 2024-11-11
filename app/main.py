from fastapi import FastAPI
from app.db import create_all_tables
from .routers import catalogs, users, kpis, boards, dashboards


app = FastAPI(lifespan=create_all_tables)
app.include_router(users.router)
app.include_router(catalogs.router)
app.include_router(kpis.router)
app.include_router(boards.router)
app.include_router(dashboards.router)


@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}
