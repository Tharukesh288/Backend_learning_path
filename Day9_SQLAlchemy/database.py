from sqlalchemy import create_engine                     # Creates the connection to the database
from sqlalchemy.orm import sessionmaker, declarative_base# Session management and ORM base
from dotenv import load_dotenv                           # Loads variables from .env
import os                                                # Allows Python to read environment variables

load_dotenv()                                            # Load the .env file

DATABASE_URL = os.getenv("DATABASE_URL")                 # Get the PostgreSQL URL from .env

engine = create_engine(                                  # Creates the PostgreSQL engine
    DATABASE_URL
)

sessionLocal = sessionmaker(                             # Creates a new database session
    autocommit=False,
    autoflush=False,
    bind=engine                                           # This session uses our PostgreSQL engine
)

Base = declarative_base()                                # Parent class for every SQLAlchemy model


def get_db():
    db = sessionLocal()                                  # Create a new database session

    try:
        yield db                                         # Give the session to FastAPI

    finally:
        db.close()                                       # Always close the session