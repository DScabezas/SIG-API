from fastapi import FastAPI
from app.models.users import User

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Dario!"}

@app.post("/users")
async def create_user(user_data: User):
    return user_data
