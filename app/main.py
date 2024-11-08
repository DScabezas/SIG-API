
from fastapi import FastAPI
from datetime import datetime
import zoneinfo

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Dario!"}
