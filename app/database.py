from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv() #load enviroment variables from .env file
DATABASE_URL = os.getenv("DATABASE_URL") #Get database url from .env file
print("🔌 DATABASE_URL from .env:", DATABASE_URL)


DATABASE_URL = os.getenv("DATABASE_URL") #Get database url from .env file
engine = create_engine(DATABASE_URL) # create engine using database url

SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine) # Create session for interacting with the DB

Base = declarative_base() #create a base class for the models.

