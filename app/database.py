from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print("🔌 DATABASE_URL from .env:", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    connection = engine.connect()
    connection.close()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection error: {str(e)}")
    print(traceback.format_exc())
    raise

# Create session factory with corrected parameter name
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()