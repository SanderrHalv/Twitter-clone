import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
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

# Pydantic model for user registration input
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # In production, hash this password before storing!

@app.post("/tweets")
def create_tweet(tweet: dict, db: Session = Depends(get_db)):
    new_tweet = Tweet(content=tweet.get("content"))
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)
    return {"message": "Tweet created", "tweet": {"id": new_tweet.id, "content": new_tweet.content}}

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": [{"id": user.id, "username": user.username, "email": user.email} for user in users]}

@app.get("/")
def read_root():
    return {"message": "Welcome to your Twitter clone API!"}

@app.get("/tweets")
def list_tweets():
    # This is a placeholder. Later, you’ll fetch tweets from the database.
    return {"tweets": []}

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logging.info("Registration endpoint called")
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    logging.info("User existence check done")
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    new_user = User(username=user.username, email=user.email, password_hash=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logging.info("User registered successfully")
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}