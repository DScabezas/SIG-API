from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_all_tables
from app.routers import boards, records, users, catalogs, dashboards, kpis, utils

app = FastAPI(lifespan=create_all_tables)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    users.router,
    boards.router,
    catalogs.router,
    dashboards.router,
    kpis.router,
    records.router,
    utils.router,
]

for router in routers:
    app.include_router(router)


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raíz de la aplicación FastAPI.

    Retorna un mensaje JSON simple para confirmar que la API está en funcionamiento.
    """
    return {"message": "Hola, Mundo!"}
