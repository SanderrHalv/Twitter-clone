from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/tweets", tags=["Tweets"])

 #Get DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@router.post("/{account_id}", response_model=schemas.Tweet)
def create_tweet(account_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    return crud.create_tweet(db, tweet, account_id)

@router.get("/", response_model=list[schemas.Tweet])
def list_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tweets(db, skip=skip, limit=limit)


    
