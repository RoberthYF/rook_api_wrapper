# app/main.py

from fastapi import FastAPI
from app.routes import router as dog_router

app = FastAPI()

app.include_router(dog_router)


@app.get("/")
def read_root():
    return {"message": "The rook API is active"}
