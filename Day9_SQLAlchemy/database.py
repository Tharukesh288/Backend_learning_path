from sqlalchemy import create_engine                     # connection manager to the database   
from sqlalchemy.orm import sessionmaker, declarative_base# every database model must inherit from one common parent that is declarative_base,
from pathlib import Path

DATABASE_URL = "sqlite:///books.db"                     #tells SQLAlchemy where the database is

engine = create_engine(                                 # creates the connection to SQLite
    DATABASE_URL,
    connect_args={"check_same_thread":False}            # allows FastAPI to use SQLite across multiple requests
)

sessionLocal = sessionmaker(                            #creates a new database session whenever we need one.
    autocommit = False,
    autoflush = False,
    bind=engine                                         # This session will use our database engine.
)

Base = declarative_base()                               # Every SQLAlchemy model will inherit from it or parent class for every ORM model

def get_db():
    db = sessionLocal()                                 # Create a new database session

    try:
        yield db                                        # Give the session to FastAPI

    finally:
        db.close()                                      # Always close the session after the request finishes