from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/tweets", tags=["Tweets"]) #create tweet router. All endpoints wil start with "/tweets"

 #Get DB dependency automaticcaly open and close DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

# Endpoint: "POST /tweets/{account_id}"
@router.post("/{account_id}", response_model=schemas.Tweet)
def create_tweet(account_id: int, tweet: schemas.TweetCreate, db: Session = Depends(get_db)):
    return crud.create_tweet(db, tweet, account_id)

@router.get("/", response_model=list[schemas.Tweet]) # list all tweets, endpoint: GET /tweets/
def list_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tweets(db, skip=skip, limit=limit)

@router.get("/search") # 
def search_tweets(keyword: str, db: Session = Depends(get_db)):
    tweets = crud.get_tweets(db)
    return [t for t in tweets if keyword.lower() in t.content.lower()]

@router.get("hashtags/{tag}")
def search_hashtags(tag: str, db: Session = Depends(get_db)):
    tweets = crud.get_tweets(db)
    return [t for t in tweets if f"#{tag.lower()}" in t.content.lower()]

@router.put("/{tweet_id}")
def update_tweet(tweet_id: int, content: str, db: Session = Depends(get_db)):
    tweet = crud.update_tweet(db, tweet_id, content)
    if not tweet:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return tweet

@router.delete("/{tweet_id}")
def delete_tweet(tweet_id: int, db: Session = Depends(get_db)):
    tweet = crud.delete_tweet(db, tweet_id)
