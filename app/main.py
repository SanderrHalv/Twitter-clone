from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers import accounts, tweets

# Lager databasen og tabellene
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Twitter Clone API")

# Inkluder routers
app.include_router(accounts.router)
app.include_router(tweets.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Clone API"}