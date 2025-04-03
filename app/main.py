from fastapi import FastAPI
from app.database import Base, engine
from app import models
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Clone API"}