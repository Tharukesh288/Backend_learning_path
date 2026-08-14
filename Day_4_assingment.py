from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

books = [
    {
        "title": "Python",
        "author": "Alex",
        "pages": 300,
        "price": 500,
        "book_id": 101
    }
]

booklist = [
    {"title": "Python", "author": "Alex", "pages": 300},
    {"title": "FastAPI", "author": "John", "pages": 250},
    {"title": "Django", "author": "John", "pages": 500},
]

class Book(BaseModel):
    title:str
    author:str
    pages:int

@app.post("/books")
def add_book(addbook:Book):
    books.append(addbook)

    if addbook is True:
        raise HTTPException(
            status_code=201,
            detail="Book added"
        )
    
    return {
        "message":"book added successfully",
        "book":addbook
    }

@app.get("/allbooks")
def get_books():
    return books

@app.get("/booklist")
def get_books(author:Optional[str]=None,    # this says that it can either be str or None by creating "Optional"
              pages:Optional[int]=None
              ):

    result = []
    for book in booklist:

        if author is not None and book["author"]!=author:
            continue

        if pages is not None and book["pages"]!=pages:
            continue

        result.append(book)
    return result

class BookResponse(BaseModel):
    title:str
    author:str
    pages:int

@app.get("/book-resopone-model",response_model=list[BookResponse])
def get_book():
    return books