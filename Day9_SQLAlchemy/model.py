from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Author(Base):
    __tablename__ = "author"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

    books = relationship("Book",back_populates="author")        # One author can have many books



class Book(Base):
    __tablename__ = "books"                                     # tells SQLAlchemy the SQL table name

    id = Column(Integer,primary_key = True, index = True)       # primary key column with an index for faster searches
    title = Column(String, nullable = False)
    pages = Column(Integer, nullable = False)
    price = Column(Float, nullable = False)
    description = Column(String, nullable=True)
    
    author_id = Column(Integer,ForeignKey("author.id"))         # Connect this book to an author

    author = relationship("Author",back_populates="books")      # Connect Python object to Author object

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String,default="user")

