from fastapi import FastAPI
from app.db import create_all_tables
from app.routers import boards, users, catalogs, dashboards, kpis


app = FastAPI(lifespan=create_all_tables)
app.include_router(users.router)
app.include_router(boards.router)
app.include_router(catalogs.router)
app.include_router(dashboards.router)
app.include_router(kpis.router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hola, Mundo!"}
