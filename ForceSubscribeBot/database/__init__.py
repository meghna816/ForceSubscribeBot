#__init__.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Base class for models
BASE = declarative_base()

# Function to start a session
def start() -> scoped_session:
    try:
        # Create the engine with connection pooling
        engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=1800)
        
        # Bind the engine to the Base metadata
        BASE.metadata.bind = engine
        
        # Create all tables in the database
        BASE.metadata.create_all(engine)
        
        # Return a scoped session for thread safety
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
    
    except SQLAlchemyError as e:
        # Log or print the error for debugging
        print(f"Error while connecting to the database: {str(e)}")
        raise e

# Start a session
SESSION = start()
