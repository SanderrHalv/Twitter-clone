from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, User, Tweet, Base, engine

app = FastAPI()

# This creates all tables defined in your models if they do not already exist.
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tweets")
def create_tweet(tweet: dict, db: Session = Depends(get_db)):
    new_tweet = Tweet(content=tweet.get("content"))
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return {"message": "Tweet created", "tweet": {"id": new_tweet.id, "content": new_tweet.content}}

@app.get("/")
def read_root():
    return {"message": "Welcome to your Twitter clone API!"}

@app.get("/tweets")
def list_tweets():
    # This is a placeholder. Later, you’ll fetch tweets from the database.
    return {"tweets": []}
