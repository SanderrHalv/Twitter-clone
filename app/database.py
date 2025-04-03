from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv() #load enviroment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL") #Get database url from .env file

engine = create_engine(DATABASE_URL)